from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os

mcp_server_scripts= os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Basics", "first_mcpserver.py")
venv_path = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".venv", "Scripts", "python.exe")
print(mcp_server_scripts)
print(venv_path) 

async def main():

    server_config = {
        "data_fetch_mcp_stdio": {
            "transport": "stdio",
            "command": venv_path,
            "args": [mcp_server_scripts],
            "env": {}
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