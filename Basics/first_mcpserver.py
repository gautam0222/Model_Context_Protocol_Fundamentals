from sys import path
from fastmcp import FastMCP

mcp=FastMCP()

@mcp.tool()
def fetch():
    """
    Fetches the data from the MCP server and returns it as a dictionary.
    """
    return {"status": "success"}

@mcp.tool()
def process(path:str):
    """
    Processes the data fetched from the MCP server and returns the processed data.
    """
    return {"status": "processed_data has been processed successfully at " + path}

if __name__ == "__main__":
    mcp.run(transport="stdio")
    