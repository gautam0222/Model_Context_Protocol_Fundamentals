from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os

mcp_server_scripts= os.path.join((os.path.dirname(os.path.abspath(__file__))), "first_mcpserver.py")
venv_path = os.path.join((os.path.dirname(os.path.abspath(__file__))), ".venv", "Scripts", "python.exe")
print(mcp_server_scripts)
print(venv_path)

async def main():
    # Create a MultiServerMCPClient instance
    client = MultiServerMCPClient(
    #mcp server config
    {
        "data_fetch_mcp_stdio": {
            "transport": "stdio",
            "command": "C:\\Users\\GautamSukhani\\Downloads\\MCP_Learning\\.venv\\Scripts\\python.exe",
            "args": ["C:\\Users\\GautamSukhani\\Downloads\\MCP_Learning\\Basics\\first_mcpserver.py"],
            "env": {}
        }
    }
    )

    #List the tools
    tools = await client.get_tools()
    print("Available Tools:", tools)

if __name__ == "__main__":
    asyncio.run(main())