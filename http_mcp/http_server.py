from fastmcp import FastMCP

mcp = FastMCP("HTTP Example Server")

@mcp.tool()
def get_http_status():
    """
    Fetches the data from the MCP server and returns it as a dictionary.
    """
    return {"status": "success"}

@mcp.tool()
def process_http_path(path: str):
    """
    Processes the data fetched from the MCP server and returns the processed data.
    """
    return {"status": f"Processed data at {path}"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http",host="localhost",port=8000)
