from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def main():

    client = MultiServerMCPClient(
    {
        "duckduckgo_mcp": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["duckduckgo-mcp-server"],
            "env": {}
        }
    }
    )

    #List the tools
    tools = await client.get_tools()
    
    print("Available Tools:")
    
    for tool in tools:
        print(tool.name)

    search = tools[0]

    result = await search.ainvoke({"query": "What is the weather today?"})
    print("Search Result:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
