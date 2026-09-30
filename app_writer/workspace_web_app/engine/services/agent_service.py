"""LangChain agent service — LiteLLM-backed chat model + workspace tools.

Provides:
  - ``LiteLLMChatModel``: LangChain ``BaseChatModel`` adapter that delegates
    to ``LLMProviderManager.completion()`` for multi-provider LLM access.
  - ``AgentService``: Manages per-application conversation sessions and
    streams agent events (thinking, tool_call, tool_result, message).

Requirements: 3.1, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any, AsyncIterator, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt — workspace guidelines and safety rules
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a workspace assistant with access to code generation and management tools.

## Workspace Guidelines
- Always use the provided tools before attempting manual work.
- NEVER modify generated code in generated_application/ — use generation tools to regenerate.
- NEVER run raw SQL — use the database management tools.
- NEVER use raw shell commands when a workspace tool exists for the operation.
- If a tool cannot handle a task, report the limitation rather than working around it.
- Application definitions in application_definitions/ are the source of truth.

## Safety Rules
- REFUSE destructive operations (drop database, remove entity, remove field, remove relationship) \
without explicit user confirmation.
- When the user asks to delete or remove something, ask for confirmation first.
- Always explain what a tool invocation will do before executing it.
- If an operation could cause data loss, warn the user.

## Behavior
- Be concise and direct.
- When an appName is provided in the conversation context, automatically scope all tool \
invocations to that application — the user should not need to specify it in every message.
- If no appName is set and a tool requires one, ask the user which application to target.
- Show tool results clearly and summarize outcomes.
"""


# ---------------------------------------------------------------------------
# LiteLLMChatModel — LangChain adapter over LLMProviderManager
# ---------------------------------------------------------------------------


def _get_llm_provider_manager():
    """Lazy import of LLMProviderManager singleton.

    LLMProviderManager is created in Task 11.2 and may not exist yet.
    This lazy accessor avoids import-time failures and allows the agent
    to pick up the manager once it is available.
    """
    try:
        from workspace_web_app.engine.services.llm_provider_manager import (
            LLMProviderManager,
        )
        return LLMProviderManager()
    except ImportError:
        logger.warning(
            "LLMProviderManager not available — agent LLM calls will fail "
            "until the provider manager is implemented (Task 11.2)."
        )
        return None


def _messages_to_dicts(messages: list[BaseMessage]) -> list[dict[str, str]]:
    """Convert LangChain message objects to LiteLLM-compatible dicts."""
    role_map = {
        "human": "user",
        "ai": "assistant",
        "system": "system",
        "tool": "tool",
    }
    result = []
    for msg in messages:
        role = role_map.get(msg.type, msg.type)
        entry: dict[str, Any] = {"role": role, "content": msg.content}
        # Preserve tool_call_id for ToolMessage so LiteLLM can correlate
        if isinstance(msg, ToolMessage) and hasattr(msg, "tool_call_id"):
            entry["tool_call_id"] = msg.tool_call_id
        result.append(entry)
    return result


class LiteLLMChatModel(BaseChatModel):
    """LangChain ``BaseChatModel`` backed by ``LLMProviderManager``.

    Delegates all completion calls to the provider manager, which handles
    model routing, fallback, and API key resolution via LiteLLM.

    The active model can change at runtime (Requirement 3.8) — each call
    fetches the current model from the provider manager.
    """

    model_name: str = "litellm"

    # ------------------------------------------------------------------
    # Required overrides
    # ------------------------------------------------------------------

    @property
    def _llm_type(self) -> str:
        return "litellm-chat"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Synchronous generation — wraps the async path for compatibility."""
        import asyncio

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # We're inside an async context; create a new loop in a thread.
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                result = pool.submit(
                    asyncio.run,
                    self._agenerate(messages, stop=stop, run_manager=None, **kwargs),
                ).result()
            return result

        return asyncio.run(
            self._agenerate(messages, stop=stop, run_manager=None, **kwargs)
        )

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Async generation via LLMProviderManager.completion().

        Fetches the active model at call time so runtime model switches
        (Requirement 3.8) take effect immediately.
        """
        manager = _get_llm_provider_manager()
        if manager is None:
            raise RuntimeError(
                "LLMProviderManager is not available. "
                "Ensure the provider manager module is implemented."
            )

        msg_dicts = _messages_to_dicts(messages)
        call_kwargs: dict[str, Any] = {}
        if stop:
            call_kwargs["stop"] = stop
        call_kwargs.update(kwargs)

        response = await manager.completion(messages=msg_dicts, **call_kwargs)

        # LiteLLM returns an OpenAI-compatible response object.
        content = response.choices[0].message.content or ""
        ai_message = AIMessage(content=content)

        # Propagate tool_calls if the model returned any.
        raw_tool_calls = getattr(response.choices[0].message, "tool_calls", None)
        if raw_tool_calls:
            ai_message.additional_kwargs["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in raw_tool_calls
            ]

        return ChatResult(generations=[ChatGeneration(message=ai_message)])


# ---------------------------------------------------------------------------
# AgentService — per-app conversation management + streaming events
# ---------------------------------------------------------------------------


class AgentService:
    """Manages LangChain agent sessions with per-application conversation history.

    Each application (keyed by ``appName``) gets its own isolated chat context
    (Requirement 3.4).  The agent has access to all workspace tools and
    auto-scopes tool invocations to the active application (Requirement 3.9).

    The ``chat()`` async generator yields event dicts with the following types:
      - ``thinking``: Agent is reasoning (intermediate text).
      - ``tool_call``: Agent is invoking a tool (name + arguments).
      - ``tool_result``: Tool execution result.
      - ``message``: Final agent response text.
    """

    def __init__(self) -> None:
        self.sessions: dict[str, list[BaseMessage]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_history(self, app_name: str) -> list[dict[str, str]]:
        """Return conversation history for an application as serializable dicts."""
        messages = self.sessions.get(app_name, [])
        return [
            {"role": msg.type, "content": msg.content}
            for msg in messages
            if not isinstance(msg, SystemMessage)
        ]

    def clear_history(self, app_name: str) -> None:
        """Clear conversation history for an application."""
        self.sessions.pop(app_name, None)

    async def chat(
        self, app_name: str, message: str
    ) -> AsyncIterator[dict[str, Any]]:
        """Process a user message and yield streaming agent events.

        Args:
            app_name: Application context for this conversation. Tools are
                auto-scoped to this app. Pass empty string for global context.
            message: The user's natural language message.

        Yields:
            Event dicts with ``type`` and ``data`` keys:
              - ``{"type": "thinking", "data": {"text": "..."}}``
              - ``{"type": "tool_call", "data": {"tool": "...", "args": {...}}}``
              - ``{"type": "tool_result", "data": {"tool": "...", "result": "..."}}``
              - ``{"type": "message", "data": {"text": "..."}}``
        """
        from workspace_web_app.engine.tools import get_all_tools

        # Ensure session exists
        if app_name not in self.sessions:
            self.sessions[app_name] = []

        history = self.sessions[app_name]

        # Build the system message with app context
        system_text = SYSTEM_PROMPT
        if app_name:
            system_text += (
                f"\n\n## Active Application\n"
                f"The current application context is: **{app_name}**\n"
                f"Automatically pass app=\"{app_name}\" to all tool invocations "
                f"that require an application name. The user does not need to "
                f"specify it."
            )

        system_msg = SystemMessage(content=system_text)

        # Add user message to history
        user_msg = HumanMessage(content=message)
        history.append(user_msg)

        # Yield thinking event
        yield {
            "type": "thinking",
            "data": {"text": "Processing your request..."},
        }

        # Build tools and agent
        tools = get_all_tools()
        llm = LiteLLMChatModel()

        # If the LLM supports tool calling, bind tools
        try:
            llm_with_tools = llm.bind_tools(tools)
        except Exception:
            # Fallback: some models may not support bind_tools
            llm_with_tools = llm

        # Build messages for the LLM call
        call_messages = [system_msg] + history

        # Agent loop: call LLM, execute tools, repeat until final answer
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            try:
                response = await llm_with_tools.ainvoke(call_messages)
            except Exception as exc:
                logger.error("LLM invocation failed: %s", exc)
                error_text = f"I encountered an error communicating with the LLM: {exc}"
                error_msg = AIMessage(content=error_text)
                history.append(error_msg)
                yield {"type": "message", "data": {"text": error_text}}
                return

            # Check for tool calls in the response
            tool_calls = response.additional_kwargs.get("tool_calls", [])

            if not tool_calls:
                # No tool calls — this is the final response
                final_text = response.content or ""
                history.append(AIMessage(content=final_text))
                yield {"type": "message", "data": {"text": final_text}}
                return

            # Process tool calls
            # Add the AI message (with tool calls) to history
            history.append(response)
            call_messages.append(response)

            tool_map = {t.name: t for t in tools}

            for tc in tool_calls:
                func_info = tc.get("function", tc)
                tool_name = func_info.get("name", "unknown")
                tool_args_raw = func_info.get("arguments", "{}")
                tool_call_id = tc.get("id", str(uuid.uuid4()))

                # Parse arguments
                try:
                    tool_args = json.loads(tool_args_raw) if isinstance(tool_args_raw, str) else tool_args_raw
                except json.JSONDecodeError:
                    tool_args = {}

                # Auto-scope: inject app_name if the tool expects it
                # and the user didn't provide one (Requirement 3.9)
                if app_name and "app" in _get_tool_param_names(tool_map.get(tool_name)):
                    if "app" not in tool_args or not tool_args["app"]:
                        tool_args["app"] = app_name

                yield {
                    "type": "tool_call",
                    "data": {"tool": tool_name, "args": tool_args},
                }

                # Execute the tool
                tool_result_text = await _execute_tool(
                    tool_map, tool_name, tool_args
                )

                yield {
                    "type": "tool_result",
                    "data": {"tool": tool_name, "result": tool_result_text},
                }

                # Add tool result to conversation
                tool_msg = ToolMessage(
                    content=tool_result_text,
                    tool_call_id=tool_call_id,
                )
                history.append(tool_msg)
                call_messages.append(tool_msg)

        # Max iterations reached
        fallback = "I've reached the maximum number of tool iterations. Please refine your request."
        history.append(AIMessage(content=fallback))
        yield {"type": "message", "data": {"text": fallback}}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get_tool_param_names(tool) -> set[str]:
    """Extract parameter names from a StructuredTool's input schema."""
    if tool is None:
        return set()
    try:
        schema = tool.args_schema
        if schema is not None:
            return set(schema.model_fields.keys())
    except Exception:
        pass
    return set()


async def _execute_tool(
    tool_map: dict, tool_name: str, tool_args: dict
) -> str:
    """Execute a tool by name with the given arguments.

    Returns the string result or an error message.
    """
    tool = tool_map.get(tool_name)
    if tool is None:
        return f"Error: Unknown tool '{tool_name}'"

    try:
        # StructuredTool supports both sync and async invocation
        result = await tool.ainvoke(tool_args)
        return str(result)
    except Exception as exc:
        logger.error("Tool '%s' failed: %s", tool_name, exc)
        return f"Error executing {tool_name}: {exc}"
