from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os
import sys

mcp_server_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stdio_server.py")

async def main():
    # Create a MultiServerMCPClient instance
    client = MultiServerMCPClient(
    #mcp server config
    {
        "data_fetch_mcp_stdio": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [mcp_server_script],
            "env": os.environ.copy(),
        }
    }
    )

    #List the tools
    tools = await client.get_tools()
    print("Available Tools:", tools)

if __name__ == "__main__":
    asyncio.run(main())
