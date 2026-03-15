from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
import asyncio

## Loading environment configuration settings 
load_dotenv()


async def test_function():

    ## Setup multiple MCP servers
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["./math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # Make sure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp",
                "transport": "http",
            }
        }
    )

    ## Load tools from registered MCP servers
    tools = await client.get_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")

    
    ## create a langchain agent to process user query and mcp call.
    agent = create_agent("openai:gpt-4.1", tools)

    ##----------- test math mcp server via local call -------------
    math_response = await agent.ainvoke({"messages": "what's (13 + 5) x 12?"})

    # print(math_response)

    AI_message = math_response["messages"][-1].content
    print(AI_message)


    ##----------- test weather mcp server via http -------------
    weather_response = await agent.ainvoke({"messages": "what is the weather in Houghton, MI?"})

    # print(weather_response)

    AI_message = weather_response["messages"][-1].content

    print(AI_message)


def main():
    print("Hello from langchain-mcp!")


if __name__ == "__main__":
    asyncio.run(test_function())
