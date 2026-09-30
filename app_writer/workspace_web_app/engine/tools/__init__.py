"""Engine tools package — LangChain StructuredTool wrappers for all workspace tools.

Usage::

    from workspace_web_app.engine.tools import get_all_tools
    tools = get_all_tools()  # list[StructuredTool]
"""

from langchain_core.tools import StructuredTool

from workspace_web_app.engine.tools.scaffold_tool import get_tools as _scaffold_tools
from workspace_web_app.engine.tools.crud_tool import get_tools as _crud_tools
from workspace_web_app.engine.tools.generation_tool import get_tools as _generation_tools
from workspace_web_app.engine.tools.definition_tool import get_tools as _definition_tools
from workspace_web_app.engine.tools.database_tool import get_tools as _database_tools
from workspace_web_app.engine.tools.validation_tool import get_tools as _validation_tools
from workspace_web_app.engine.tools.discussion_tool import get_tools as _discussion_tools
from workspace_web_app.engine.tools.github_crawler_tool import get_tools as _github_tools
from workspace_web_app.engine.tools.misc_tools import get_tools as _misc_tools


def get_all_tools() -> list[StructuredTool]:
    """Return a flat list of all LangChain StructuredTool instances."""
    return [
        *_scaffold_tools(),
        *_crud_tools(),
        *_generation_tools(),
        *_definition_tools(),
        *_database_tools(),
        *_validation_tools(),
        *_discussion_tools(),
        *_github_tools(),
        *_misc_tools(),
    ]
