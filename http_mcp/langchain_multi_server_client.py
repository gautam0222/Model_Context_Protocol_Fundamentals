from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mcp_server_script = os.path.join(project_root, "basics", "stdio_server.py")

async def main():

    server_config = {
        "data_fetch_mcp_stdio": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [mcp_server_script],
            "env": os.environ.copy(),
        },

        "data_fetch_mcp_http": {
            "transport": "streamable-http",
            "url": "http://localhost:8000/mcp"
        }
    }

    client = MultiServerMCPClient(server_config)

    #List the tools
    tools = await client.get_tools()
    
    print("Available Tools:")
    
    for tool in tools:
        print(tool.name)

if __name__ == "__main__":
    asyncio.run(main())
