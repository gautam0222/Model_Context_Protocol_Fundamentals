import asyncio
import os
import sys
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

mcp_server_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stdio_server.py")

#Create Server Parameters
server_params = StdioServerParameters(command=sys.executable, args=[mcp_server_script], env=os.environ.copy())

#Create a client session
async def main():
    async with stdio_client(server_params) as (reader, writer):

        async with ClientSession(reader, writer) as client_session:

            await client_session.initialize()

            #Fetch tools
            tools = await client_session.list_tools()
            print("Available Tools:", tools)    

            result = await client_session.call_tool("process_path", arguments={"path": "path/to/data"})
            print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
