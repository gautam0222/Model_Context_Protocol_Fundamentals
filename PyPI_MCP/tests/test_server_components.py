import asyncio

import learning_mcp.main  # Registers resources and prompts with the shared server.
from learning_mcp.tools import mcp


def test_server_registers_learning_components():
    resources = asyncio.run(mcp.get_resources())
    templates = asyncio.run(mcp.get_resource_templates())
    prompts = asyncio.run(mcp.get_prompts())

    assert "workspace://guide" in resources
    assert "workspace://files/{relative_path}" in templates
    assert "summarize_workspace_file" in prompts
    assert "plan_safe_file_change" in prompts
