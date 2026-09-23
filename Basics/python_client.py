import os
import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession,StdioServerParameters, client

mcp_server_scripts= os.path.join((os.path.dirname(os.path.abspath(__file__))), "first_mcpserver.py")

print(mcp_server_scripts)

#Create Server Parameters
server_params = StdioServerParameters(command="python",args=[str(mcp_server_scripts)],env={})

#Create a client session
async def main():
    async with stdio_client(server_params) as (reader, writer):

        async with ClientSession(reader, writer) as client_session:

            await client_session.initialize()

            #Fetch tools
            tools = await client_session.list_tools()
            print("Available Tools:", tools)    

            result = await client_session.call_tool("process", arguments={"path": "path/to/data"})
            print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())