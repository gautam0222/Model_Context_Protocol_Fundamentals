"""Reusable MCP prompts for common learning tasks."""

from learning_mcp.tools import mcp


@mcp.prompt(
    name="summarize_workspace_file",
    description="Guide an assistant to summarize a file with the read_text_file tool.",
)
def summarize_workspace_file(relative_path: str) -> str:
    """Create a user-controlled prompt for understanding a workspace file."""
    return f"""Read `{relative_path}` with the `read_text_file` tool.
Then explain its purpose, the important parts, and one beginner-friendly improvement.
If the file cannot be read, explain the error and do not guess its contents."""


@mcp.prompt(
    name="plan_safe_file_change",
    description="Create a cautious plan for editing a file in the workspace.",
)
def plan_safe_file_change(relative_path: str, goal: str) -> str:
    """Create a reusable prompt that encourages review before writes."""
    return f"""I want to change `{relative_path}` to achieve this goal: {goal}

First read the file. Explain a small plan, then ask for confirmation before using
`write_text_file` with `overwrite=true`. Keep all work inside the configured workspace."""
