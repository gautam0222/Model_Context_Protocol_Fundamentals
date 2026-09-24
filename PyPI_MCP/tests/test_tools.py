import pytest

from learning_mcp import tools


@pytest.fixture()
def workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "WORKSPACE", tmp_path)
    return tmp_path


def test_workspace_path_rejects_parent_directory(workspace):
    with pytest.raises(ValueError, match="stay inside"):
        tools.workspace_path("../outside.txt")


def test_write_read_and_list_files(workspace):
    result = tools.write_workspace_text("notes/hello.txt", "Hello MCP")

    assert result == "Wrote 9 characters to notes/hello.txt."
    assert tools.read_workspace_text("notes/hello.txt") == "Hello MCP"
    assert tools.list_workspace_files("notes") == ["hello.txt"]


def test_existing_file_requires_explicit_overwrite(workspace):
    tools.write_workspace_text("note.txt", "first")

    with pytest.raises(ValueError, match="overwrite"):
        tools.write_workspace_text("note.txt", "second")

    tools.write_workspace_text("note.txt", "second", overwrite=True)
    assert tools.read_workspace_text("note.txt") == "second"


def test_search_returns_relative_path_and_line_number(workspace):
    tools.write_workspace_text("guide.txt", "First line\nMCP is useful\nLast line")

    assert tools.search_workspace_text("mcp") == ["guide.txt:2: MCP is useful"]
