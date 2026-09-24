"""Read-only MCP resources for the learning server."""

from learning_mcp.tools import WORKSPACE, mcp, read_workspace_text


@mcp.resource(
    "workspace://guide",
    name="learning_guide",
    description="A short guide to the tools, prompts, and workspace rules in this server.",
    mime_type="text/markdown",
)
def learning_guide() -> str:
    """Provide introductory context that a client can attach to a conversation."""
    return f"""# Learning MCP guide

This server works only inside `{WORKSPACE}`.

- **Tools** perform actions, such as reading or writing a workspace file.
- **Resources** provide read-only context, such as this guide or a text file.
- **Prompts** provide reusable instructions for a user-selected task.

Use `write_text_file` with `overwrite=true` only when you intend to replace a file.
"""


@mcp.resource(
    "workspace://files/{relative_path}",
    name="workspace_text_file",
    description="Read a UTF-8 text file from the configured workspace.",
    mime_type="text/plain",
)
def workspace_text_file(relative_path: str) -> str:
    """Expose a workspace file as a read-only, parameterized resource."""
    return read_workspace_text(relative_path)
