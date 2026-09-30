"""Generation job manager — runs code generation in background threads.

Supports four generation types:
  - full, incremental, sql_only → Phase 3 (phase3_definition_first.py)
  - react → REAW via subprocess (run_tool_subprocess)

Each output line is published to the ``events.jobs`` Kafka topic with a
sequence number.  Completion or failure is published as a final event.
Active jobs are tracked per-application to reject duplicate starts.
"""

from __future__ import annotations

import asyncio
import json
import logging
import subprocess
import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from workspace_web_app.engine.config import (
    APPLICATION_DEFINITIONS_DIR,
    TOOL_PATHS,
    WORKSPACE_ROOT,
)
from workspace_web_app.engine.utils.envelope import build_envelope

if TYPE_CHECKING:
    from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

EVENTS_JOBS_TOPIC = "events.jobs"

# Phase 3 flags per generation type
_PHASE3_FLAGS: dict[str, str] = {
    "full": "--full",
    "incremental": "--skip-sql",
    "sql_only": "--skip-java",
}

VALID_GEN_TYPES = {"full", "incremental", "sql_only", "react"}


class JobStatus(str, Enum):
    """Lifecycle states for a generation job."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class GenerationJob:
    """Tracks a single generation job's state.

    Attributes:
        job_id: Unique identifier for this job.
        app_name: Application this job generates code for.
        gen_type: One of ``full``, ``incremental``, ``sql_only``, ``react``.
        status: Current lifecycle status.
        output_lines: Captured stdout lines from the generation process.
        cancel_requested: Flag checked by the worker thread to abort early.
        error: Error message if the job failed.
        generated_files: List of files produced on success (populated at completion).
    """

    job_id: str
    app_name: str
    gen_type: str
    status: JobStatus = JobStatus.PENDING
    output_lines: list[str] = field(default_factory=list)
    cancel_requested: bool = False
    error: str | None = None
    generated_files: list[str] = field(default_factory=list)


class JobManager:
    """Manages generation jobs running in background threads.

    One job per application at a time.  Each stdout line is published to
    ``events.jobs`` as a ``job_output`` event with a sequence number.
    Completion or failure is published as ``job_completed`` / ``job_failed``.
    """

    def __init__(self) -> None:
        self._jobs: dict[str, GenerationJob] = {}
        # Maps app_name → active job_id to enforce one-job-per-app.
        self._active_by_app: dict[str, str] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start_job(
        self,
        app: str,
        gen_type: str,
        producer: AIOKafkaProducer,
        correlation_id: str | None = None,
        session_id: str = "",
    ) -> str:
        """Start a generation job in a background thread.

        Args:
            app: Application name (must exist in application_definitions/).
            gen_type: One of ``full``, ``incremental``, ``sql_only``, ``react``.
            producer: Kafka producer for publishing progress events.
            correlation_id: Optional correlation ID; auto-generated if *None*.
            session_id: Browser session identifier.

        Returns:
            The ``job_id`` for the newly started job.

        Raises:
            ValueError: If *gen_type* is invalid or a job is already running
                for *app*.
        """
        if gen_type not in VALID_GEN_TYPES:
            raise ValueError(
                f"Invalid generation type '{gen_type}'. "
                f"Must be one of: {', '.join(sorted(VALID_GEN_TYPES))}"
            )

        with self._lock:
            if app in self._active_by_app:
                existing_id = self._active_by_app[app]
                existing = self._jobs.get(existing_id)
                if existing and existing.status == JobStatus.RUNNING:
                    raise ValueError(
                        f"A generation job is already running for '{app}' "
                        f"(job_id={existing_id})"
                    )

            job_id = correlation_id or str(uuid.uuid4())
            job = GenerationJob(
                job_id=job_id,
                app_name=app,
                gen_type=gen_type,
                status=JobStatus.PENDING,
            )
            self._jobs[job_id] = job
            self._active_by_app[app] = job_id

        # Capture the running event loop so the worker thread can schedule
        # async publishes back onto it.
        loop = asyncio.get_running_loop()

        thread = threading.Thread(
            target=self._run_job,
            args=(job, producer, loop, session_id),
            daemon=True,
            name=f"gen-{job_id[:8]}",
        )
        thread.start()

        logger.info(
            "Started %s generation job %s for app '%s'",
            gen_type,
            job_id,
            app,
        )
        return job_id

    def cancel_job(self, job_id: str) -> bool:
        """Request cancellation of a running job.

        Args:
            job_id: The job to cancel.

        Returns:
            *True* if the cancellation flag was set, *False* if the job
            was not found or not in a cancellable state.
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return False
            if job.status not in (JobStatus.PENDING, JobStatus.RUNNING):
                return False
            job.cancel_requested = True
        logger.info("Cancellation requested for job %s", job_id)
        return True

    def get_job_status(self, job_id: str) -> dict:
        """Return the current status of a job.

        Args:
            job_id: The job to query.

        Returns:
            Dict with ``job_id``, ``app_name``, ``gen_type``, ``status``,
            ``line_count``, ``error``, and ``generated_files``.

        Raises:
            KeyError: If *job_id* is unknown.
        """
        job = self._jobs.get(job_id)
        if job is None:
            raise KeyError(f"Unknown job_id: {job_id}")
        return {
            "job_id": job.job_id,
            "app_name": job.app_name,
            "gen_type": job.gen_type,
            "status": job.status.value,
            "line_count": len(job.output_lines),
            "error": job.error,
            "generated_files": job.generated_files,
        }

    # ------------------------------------------------------------------
    # Internal — worker thread
    # ------------------------------------------------------------------

    def _run_job(
        self,
        job: GenerationJob,
        producer: AIOKafkaProducer,
        loop: asyncio.AbstractEventLoop,
        session_id: str,
    ) -> None:
        """Execute the generation subprocess and stream output lines.

        Runs in a daemon thread.  Each stdout line is published to Kafka
        via the event loop of the main async thread.
        """
        job.status = JobStatus.RUNNING
        seq = 0

        # Publish a "job_started" event
        self._publish(
            loop,
            producer,
            "job_started",
            {
                "job_id": job.job_id,
                "app_name": job.app_name,
                "gen_type": job.gen_type,
            },
            job,
            session_id,
        )

        try:
            command = self._build_command(job.app_name, job.gen_type)
            logger.info("Job %s running: %s", job.job_id, command)

            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=WORKSPACE_ROOT,
            )

            for line in iter(proc.stdout.readline, ""):
                if job.cancel_requested:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    job.status = JobStatus.CANCELLED
                    self._publish(
                        loop,
                        producer,
                        "job_cancelled",
                        {
                            "job_id": job.job_id,
                            "app_name": job.app_name,
                            "line_count": len(job.output_lines),
                        },
                        job,
                        session_id,
                    )
                    self._cleanup_active(job)
                    return

                stripped = line.rstrip("\n")
                job.output_lines.append(stripped)
                seq += 1

                self._publish(
                    loop,
                    producer,
                    "job_output",
                    {
                        "job_id": job.job_id,
                        "app_name": job.app_name,
                        "line": stripped,
                        "seq": seq,
                    },
                    job,
                    session_id,
                )

            proc.wait()

            if proc.returncode != 0:
                error_msg = f"Process exited with code {proc.returncode}"
                job.error = error_msg
                job.status = JobStatus.FAILED
                self._publish(
                    loop,
                    producer,
                    "job_failed",
                    {
                        "job_id": job.job_id,
                        "app_name": job.app_name,
                        "error": error_msg,
                        "line_count": len(job.output_lines),
                    },
                    job,
                    session_id,
                )
            else:
                job.status = JobStatus.COMPLETED
                self._publish(
                    loop,
                    producer,
                    "job_completed",
                    {
                        "job_id": job.job_id,
                        "app_name": job.app_name,
                        "gen_type": job.gen_type,
                        "line_count": len(job.output_lines),
                        "generated_files": job.generated_files,
                    },
                    job,
                    session_id,
                )

        except Exception as exc:
            job.error = str(exc)
            job.status = JobStatus.FAILED
            logger.exception("Job %s failed with exception", job.job_id)
            self._publish(
                loop,
                producer,
                "job_failed",
                {
                    "job_id": job.job_id,
                    "app_name": job.app_name,
                    "error": str(exc),
                    "line_count": len(job.output_lines),
                },
                job,
                session_id,
            )
        finally:
            self._cleanup_active(job)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_command(app_name: str, gen_type: str) -> list[str]:
        """Build the subprocess command list for a generation type.

        Phase 3 types (full, incremental, sql_only) invoke
        ``phase3_definition_first.py``.  React invokes REAW via
        ``run_tool_subprocess`` style command.

        Args:
            app_name: Target application name.
            gen_type: One of the VALID_GEN_TYPES.

        Returns:
            Command as a list of strings suitable for ``subprocess.Popen``.
        """
        if gen_type == "react":
            reaw_path = TOOL_PATHS["reaw"]
            app_defs = f"{APPLICATION_DEFINITIONS_DIR}/{app_name}"
            output_dir = f"{WORKSPACE_ROOT}/generated_application/{app_name}/react_app"
            return [
                "python",
                reaw_path,
                "--input",
                app_defs,
                "--output",
                output_dir,
            ]

        # Phase 3 generation types
        phase3_path = TOOL_PATHS["phase3"]
        flag = _PHASE3_FLAGS[gen_type]
        output_dir = f"{WORKSPACE_ROOT}/generated_application/{app_name}"
        return [
            "python",
            phase3_path,
            "--app",
            app_name,
            "--output",
            output_dir,
            flag,
        ]

    def _publish(
        self,
        loop: asyncio.AbstractEventLoop,
        producer: AIOKafkaProducer,
        event_type: str,
        payload: dict,
        job: GenerationJob,
        session_id: str,
    ) -> None:
        """Schedule a Kafka publish on the main event loop (thread-safe).

        Uses ``build_envelope`` so every message follows the standard
        Kafka envelope format.
        """
        envelope = build_envelope(
            type=event_type,
            payload=payload,
            correlation_id=job.job_id,
            session_id=session_id,
            app_name=job.app_name,
        )
        future = asyncio.run_coroutine_threadsafe(
            producer.send_and_wait(
                EVENTS_JOBS_TOPIC,
                json.dumps(envelope).encode("utf-8"),
            ),
            loop,
        )
        try:
            future.result(timeout=10)
        except Exception:
            logger.warning(
                "Failed to publish %s for job %s", event_type, job.job_id
            )

    def _cleanup_active(self, job: GenerationJob) -> None:
        """Remove the app → job mapping when a job finishes."""
        with self._lock:
            if self._active_by_app.get(job.app_name) == job.job_id:
                del self._active_by_app[job.app_name]
