"""Property-based tests for StatusTracker dirty tracking accuracy.

**Validates: Requirements 4.1, 4.2, 4.6**
"""

import json
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from app_def_manager.status_tracker import StatusTracker


# --- Strategies ---

# Generate valid filenames that look like definition files
_filename_st = st.from_regex(r"webflux_[a-z]{1,12}\.json", fullmatch=True)

# Generate a non-empty list of unique filenames (the "all files" universe)
_unique_filenames_st = st.lists(
    _filename_st, min_size=2, max_size=8, unique=True
)


def _create_files_on_disk(app_dir: Path, filenames: list[str]) -> None:
    """Create actual definition files on disk so SHA-256 hashing works."""
    app_dir.mkdir(parents=True, exist_ok=True)
    for fname in filenames:
        (app_dir / fname).write_text(json.dumps({"file": fname}), encoding="utf-8")


# --- Property 12: Dirty tracking accuracy ---


@settings(max_examples=20)
@given(data=st.data())
def test_dirty_tracking_accuracy(data: st.DataObject) -> None:
    """Property 12: Dirty tracking accuracy

    For any list of filenames marked dirty, get_dirty_files() returns exactly
    those files, and unmarked files retain previous status.

    **Validates: Requirements 4.1, 4.2, 4.6**
    """
    # Draw a universe of unique filenames
    all_files = data.draw(_unique_filenames_st, label="all_files")

    # Split into dirty subset and remaining (clean) subset
    dirty_indices = data.draw(
        st.lists(
            st.integers(min_value=0, max_value=len(all_files) - 1),
            min_size=1,
            max_size=len(all_files),
            unique=True,
        ),
        label="dirty_indices",
    )
    dirty_files = [all_files[i] for i in dirty_indices]
    clean_files = [f for f in all_files if f not in dirty_files]

    with tempfile.TemporaryDirectory() as tmp:
        app_dir = Path(tmp) / "test_app"

        # Create real files on disk (needed for SHA-256 hashing)
        _create_files_on_disk(app_dir, all_files)

        tracker = StatusTracker(app_dir)

        # Initialize all files as clean first
        tracker.create_initial_status(all_files)
        tracker.mark_clean(all_files)

        # Verify all start clean
        assert set(tracker.get_clean_files()) == set(all_files)
        assert tracker.get_dirty_files() == []

        # Now mark the dirty subset as dirty
        tracker.mark_dirty(dirty_files)

        # Property: get_dirty_files() returns exactly the dirty subset
        reported_dirty = set(tracker.get_dirty_files())
        assert reported_dirty == set(dirty_files), (
            f"Expected dirty={set(dirty_files)}, got {reported_dirty}"
        )

        # Property: unmarked files retain their previous (clean) status
        reported_clean = set(tracker.get_clean_files())
        assert reported_clean == set(clean_files), (
            f"Expected clean={set(clean_files)}, got {reported_clean}"
        )

        # Property: each dirty file has updated last_modified and content_hash (Req 4.2)
        status = tracker.load()
        for fname in dirty_files:
            info = status["files"][fname]
            assert info["status"] == "dirty"
            assert info["last_modified"] is not None
            assert info["content_hash"].startswith("sha256:")

        # Property: each clean file retains status unchanged (Req 4.6)
        for fname in clean_files:
            info = status["files"][fname]
            assert info["status"] == "clean"


# --- Property 13: Status file convergence after full generation ---


@settings(max_examples=20)
@given(all_files=_unique_filenames_st)
def test_status_convergence_after_full_generation(all_files: list[str]) -> None:
    """Property 13: Status file convergence after full generation

    After mark_all_clean(), all tracked files have status "clean" with
    updated last_generated timestamps.

    **Validates: Requirements 4.3, 4.7**
    """
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = Path(tmp) / "test_app"

        # Create real files on disk (needed for SHA-256 hashing)
        _create_files_on_disk(app_dir, all_files)

        tracker = StatusTracker(app_dir)

        # Initialize all files as dirty (simulates pre-generation state)
        tracker.create_initial_status(all_files)

        # Verify all start dirty with no last_generated
        status_before = tracker.load()
        for fname in all_files:
            info = status_before["files"][fname]
            assert info["status"] == "dirty"
            assert info["last_generated"] is None

        # Simulate successful full generation → mark all clean
        tracker.mark_all_clean()

        # Property: every tracked file now has status "clean"
        status_after = tracker.load()
        for fname in all_files:
            info = status_after["files"][fname]
            assert info["status"] == "clean", (
                f"Expected '{fname}' to be clean after mark_all_clean(), "
                f"got '{info['status']}'"
            )

        # Property: every tracked file has a non-null last_generated timestamp
        for fname in all_files:
            info = status_after["files"][fname]
            assert info["last_generated"] is not None, (
                f"Expected '{fname}' to have last_generated set after "
                f"mark_all_clean(), got None"
            )

        # Property: no files remain dirty
        assert tracker.get_dirty_files() == [], (
            f"Expected no dirty files after mark_all_clean(), "
            f"got {tracker.get_dirty_files()}"
        )

        # Property: all files are reported as clean
        assert set(tracker.get_clean_files()) == set(all_files), (
            f"Expected all files clean, got {set(tracker.get_clean_files())}"
        )
