"""Tools for a deliberately small, workspace-limited learning MCP server."""

import os
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("Learning MCP")
WORKSPACE = Path(os.getenv("MCP_WORKSPACE", Path.cwd())).resolve()


def workspace_path(relative_path: str = ".") -> Path:
    """Resolve a path and prevent tools from leaving MCP_WORKSPACE."""
    candidate = (WORKSPACE / relative_path).resolve()
    if candidate != WORKSPACE and WORKSPACE not in candidate.parents:
        raise ValueError("Path must stay inside the configured workspace.")
    return candidate


def list_workspace_files(relative_path: str = ".") -> list[str]:
    """List the direct children of a workspace folder."""
    path = workspace_path(relative_path)
    if not path.is_dir():
        raise ValueError(f"Not a folder: {relative_path}")
    return [item.name + ("/" if item.is_dir() else "") for item in sorted(path.iterdir())]


def read_workspace_text(relative_path: str) -> str:
    """Read a UTF-8 text file after checking its workspace path."""
    path = workspace_path(relative_path)
    if not path.is_file():
        raise ValueError(f"Not a file: {relative_path}")
    return path.read_text(encoding="utf-8")


def write_workspace_text(relative_path: str, content: str, overwrite: bool = False) -> str:
    """Create or deliberately replace a UTF-8 workspace text file."""
    path = workspace_path(relative_path)
    if path.exists() and not overwrite:
        raise ValueError("File already exists. Set overwrite=true to replace it.")
    if path.is_dir():
        raise ValueError(f"Cannot write to a folder: {relative_path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {relative_path}."


def search_workspace_text(query: str, relative_path: str = ".") -> list[str]:
    """Search UTF-8 files in the workspace and return matching lines."""
    start = workspace_path(relative_path)
    if not start.exists():
        raise ValueError(f"Path does not exist: {relative_path}")
    files = [start] if start.is_file() else (path for path in start.rglob("*") if path.is_file())
    matches: list[str] = []
    for path in files:
        try:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if query.lower() in line.lower():
                    matches.append(f"{path.relative_to(WORKSPACE)}:{number}: {line}")
        except UnicodeDecodeError:
            continue
    return matches


@mcp.tool()
def get_workspace_info() -> dict[str, str]:
    """Return the workspace that all file tools are limited to."""
    return {"workspace": str(WORKSPACE), "message": "Set MCP_WORKSPACE to use another folder."}


@mcp.tool()
def list_files(relative_path: str = ".") -> list[str]:
    """List files and folders directly inside a workspace folder."""
    return list_workspace_files(relative_path)


@mcp.tool()
def read_text_file(relative_path: str) -> str:
    """Read a UTF-8 text file inside the workspace."""
    return read_workspace_text(relative_path)


@mcp.tool()
def write_text_file(relative_path: str, content: str, overwrite: bool = False) -> str:
    """Create a UTF-8 file. Set overwrite to true only when replacing an existing file."""
    return write_workspace_text(relative_path, content, overwrite)


@mcp.tool()
def create_folder(relative_path: str) -> str:
    """Create a folder inside the workspace."""
    path = workspace_path(relative_path)
    path.mkdir(parents=True, exist_ok=True)
    return f"Folder ready: {relative_path}"


@mcp.tool()
def search_text(query: str, relative_path: str = ".") -> list[str]:
    """Find case-insensitive text matches in workspace text files, with line numbers."""
    return search_workspace_text(query, relative_path)
    
