# MCP Learning

This repository is a Python learning project for the **Model Context Protocol (MCP)**. It is a progression of small examples rather than one production application: local servers, clients, HTTP transport, external servers, gateway composition, Docker, and an installable custom server.

## MCP fundamentals

MCP is a standard protocol through which an AI application discovers and uses capabilities supplied by another program. It separates the application that hosts an AI experience from the services that provide useful context or actions.

| Role   | Responsibility                                                        | Example here                                 |
| ------ | --------------------------------------------------------------------- | -------------------------------------------- |
| Host   | The AI application that manages user interaction and MCP connections. | An MCP-enabled desktop application or agent. |
| Client | Connects to servers, discovers capabilities, and invokes them.        | basics/stdio_client.py                       |
| Server | Exposes capabilities in MCP's standard format.                        | pypi_mcp                                     |

```text
User → Host / AI application → MCP client → MCP server → result → Host
```

MCP does not choose the model or build the chat interface. It standardizes the boundary between an AI application and its tools or context providers.

## Tools, resources, and prompts

These are MCP's three main primitives. Choosing the right one is an important design decision.

| Primitive | Normally selected by          | Purpose                                                  | Example in this repository   |
| --------- | ----------------------------- | -------------------------------------------------------- | ---------------------------- |
| Tool      | Model, subject to host policy | Performs an action or returns a computed result.         | write_text_file, search_text |
| Resource  | Host application              | Supplies read-only context identified by a URI.          | workspace://guide            |
| Prompt    | User                          | Supplies a reusable, parameterized instruction workflow. | summarize_workspace_file     |

### Tools

A tool is a server function. FastMCP turns functions decorated with @mcp.tool() into discoverable tool definitions. Python type hints describe tool inputs, so write_text_file(relative_path: str, content: str, overwrite: bool = False) clearly communicates its schema.

Tools may have side effects. A good tool has one narrow responsibility, validated input, a clear description, a predictable result, and safe defaults. In this project, overwriting a file requires overwrite=true; it is never the default.

### Resources

Resources are read-only content that a host can attach to a model conversation. They are identified with URIs, which makes them useful for documentation, configuration, and files.

The custom server demonstrates both forms:

- workspace://guide is a static resource containing server documentation.
- workspace://files/{relative_path} is a resource template; its URI parameter identifies one safe workspace text file.

Read-only does not mean unrestricted. Resources must respect the same access boundary as tools.

### Prompts

Prompts are reusable instruction templates chosen by a user. summarize_workspace_file guides an assistant to read and explain a file. plan_safe_file_change creates a review-first workflow that asks for confirmation before overwriting a file.

Prompts influence model behavior but do not enforce security. Input validation, server policy, and host approval are the actual controls.

## Transports

| Transport       | Description                                                                                          | Example               |
| --------------- | ---------------------------------------------------------------------------------------------------- | --------------------- |
| stdio           | The client launches a local server process and exchanges MCP messages through standard input/output. | basics                |
| Streamable HTTP | A long-running server receives MCP requests over HTTP.                                               | http_mcp, gateway_mcp |

Stdio is simple and appropriate for local tools. HTTP is useful for a service but adds authentication, authorization, logging, rate limiting, and network-exposure concerns.

## Architecture

```text
                         MCP host / AI application
                                      |
                       +--------------+--------------+
                       |                             |
                    stdio                         HTTP /mcp
                       |                             |
       basics/stdio_server.py              gateway_mcp/server.py
                                                    |
                                  +-----------------+-----------------+
                                  |                                   |
                       DuckDuckGo MCP via uvx                learning-mcp package
                                                                    |
                                                      tools + resources + prompts
```

http_mcp is a standalone HTTP transport example. community_mcp is a client-side integration example for servers maintained outside this repository. docker_mcp packages the gateway and the local package in one container.

## Repository guide

### basics

This is the smallest complete MCP exchange.

- stdio_server.py exposes get_status and process_path.
- stdio_client.py uses the lower-level MCP SDK: it starts the subprocess, initializes a ClientSession, lists tools, and calls process_path.
- langchain_stdio_client.py uses MultiServerMCPClient from LangChain to discover the same server.

The central lesson is discovery: clients can request server tool definitions rather than hard-coding every capability.

### http_mcp

http_server.py exposes equivalent demonstration tools using Streamable HTTP. langchain_multi_server_client.py connects to this HTTP server and the stdio server together, showing that one client can aggregate tools from different transports.

### community_mcp

- duckduckgo_client.py starts a community DuckDuckGo MCP server with uvx, then discovers and calls its tools.
- tavily_client.py connects to Tavily's hosted MCP endpoint using TAVILY_API_KEY from a local .env file.

These files demonstrate MCP as an integration boundary: a client can use a server it did not implement, provided it has valid connection details and credentials.

### gateway_mcp

server.py is a composition example. It exposes two local tools and mounts proxy servers for DuckDuckGo and learning-mcp using FastMCP.as_proxy.

A gateway gives a host one connection while it aggregates several downstream servers. In a real deployment it is a security boundary: it must decide which downstream servers are trusted, which tools are exposed, and how access is logged and authorized.

### docker_mcp

The Docker configuration installs DuckDuckGo's server and this repository's learning-mcp package, creates /workspace, sets it as MCP_WORKSPACE, and starts the HTTP gateway. Containers improve repeatability and make the file boundary more explicit. Mounting a host directory into /workspace is still a deliberate security choice.

## The custom learning-mcp package

pypi_mcp is the repository's complete, installable learning server.

```text
pypi_mcp/
├── pyproject.toml                 package metadata and dependencies
├── src/learning_mcp/
│   ├── main.py                    entry point and component registration
│   ├── tools.py                   workspace helpers and MCP tools
│   ├── resources.py               read-only resources
│   └── prompts.py                 reusable prompt templates
└── tests/                         focused behavior tests
```

The package distribution is learning-mcp, its Python import package is learning_mcp, and its command is learning-mcp. main.py imports the resources and prompts modules deliberately: their decorators register those components with the shared FastMCP server before it starts.

### Workspace safety boundary

All filesystem operations are restricted to MCP_WORKSPACE; if that variable is absent, the server uses its current working directory.

```text
requested relative path
        ↓
resolve beneath MCP_WORKSPACE
        ↓
reject path if it escapes the workspace
```

workspace_path enforces this rule. It rejects paths such as ../outside.txt. The project deliberately removed unrestricted shell execution, arbitrary Python execution, and recursive deletion because they are unsafe capabilities to expose to an AI-connected client.

### Tools

Internal helpers perform the filesystem work, and public FastMCP tools call those helpers. This makes behavior easy to test without a running server.

| Tool               | Description                       | Safety behavior                                                               |
| ------------------ | --------------------------------- | ----------------------------------------------------------------------------- |
| get_workspace_info | Returns the active workspace.     | Makes the boundary visible.                                                   |
| list_files         | Lists direct folder contents.     | Restricted to the workspace.                                                  |
| read_text_file     | Reads one UTF-8 text file.        | Rejects missing files and folders.                                            |
| write_text_file    | Creates or replaces a UTF-8 file. | Requires overwrite=true to replace.                                           |
| create_folder      | Creates a folder and parents.     | Safe to repeat.                                                               |
| search_text        | Searches text recursively.        | Returns relative path, line number, and matching line; skips non-UTF-8 files. |

### Resources and prompts

| Capability                        | Type              | Purpose                                                    |
| --------------------------------- | ----------------- | ---------------------------------------------------------- |
| workspace://guide                 | Resource          | Provides read-only documentation context.                  |
| workspace://files/{relative_path} | Resource template | Safely exposes one workspace text file.                    |
| summarize_workspace_file          | Prompt            | Guides an assistant through reading and explaining a file. |
| plan_safe_file_change             | Prompt            | Produces a cautious plan before a destructive overwrite.   |

Use a resource for stable read-only context, a prompt for a reusable user workflow, and a tool for an action or calculation.

## Testing and dependencies

The root project uses FastMCP, LangChain, and langchain-mcp-adapters. The independently packageable pypi_mcp project uses FastMCP plus pytest as a development dependency. uv.lock files record resolved versions for repeatable environments.

The pypi_mcp tests cover:

- workspace escape prevention;
- file creation, reading, and listing;
- explicit overwrite behavior;
- search result formatting;
- registration of resources, resource templates, and prompts.

The suite contains five tests and does not require a live server or external API, which keeps it fast and deterministic.
