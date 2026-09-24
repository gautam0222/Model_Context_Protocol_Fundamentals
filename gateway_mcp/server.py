from fastmcp import FastMCP

mcp = FastMCP("Learning Gateway")

@mcp.tool()
def get_gateway_status():
    """
    Fetches the data from the MCP server and returns it as a dictionary.
    """
    return {"status": "success"}

@mcp.tool()
def process_gateway_path(path: str):
    """
    Processes the data fetched from the MCP server and returns the processed data.
    """
    return {"status": f"Processed data at {path}"}

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
            "learning_mcp": {
                "command": "learning-mcp",
                "args": [],
                "env": {}
        }
        }
    })
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http",host="localhost",port=8000)
