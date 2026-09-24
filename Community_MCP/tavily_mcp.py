from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os
from typing import Any
from dotenv import load_dotenv
load_dotenv()

async def main():

    tavily_api_key = os.getenv("TAVILY_API_KEY")

    server_config: dict[str, Any] = {
        "data_fetch_mcp_stdio": {
            "transport": "streamable-http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_api_key}"
        }
    }
    client = MultiServerMCPClient(server_config)

    #List the tools
    tools = await client.get_tools()
    
    print("Available Tools:")
    
    for tool in tools:
        print(tool.name)

    tavily_search = tools[0]

    result = await tavily_search.ainvoke({"query": "Give some good research papers on machine learning?"})
    print("Search Result:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())