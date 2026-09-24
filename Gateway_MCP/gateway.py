from fastmcp import FastMCP

mcp=FastMCP()

@mcp.tool()
def fetch_http():
    """
    Fetches the data from the MCP server and returns it as a dictionary.
    """
    return {"status": "success"}

@mcp.tool()
def process_http(path:str):
    """
    Processes the data fetched from the MCP server and returns the processed data.
    """
    return {"status": "processed_data has been processed successfully at " + path}

#mount the tools to the mcp server
mcp.mount(
    FastMCP.as_proxy({
        "mcpServers":{
            "ddg_mcp": {
                "command": "uvx",
                "args": ["duckduckgo-mcp-server"],
                "env": {}
            },

        }
    })
)

mcp.mount(
    FastMCP.as_proxy({
        "mcpServers":{
            "agentic_terminal_mcp": {
                "command": "uvx",
                "args": ["agentic_terminal"],
                "env": {}
        }
        }
    })
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http",host="localhost",port=8000)