from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from dotenv import load_dotenv
import argparse
import asyncio
import os

## Loading environment configuration settings 
load_dotenv()


async def test_function(backend: int = 0):

    # 1. Setup your model
    llm_openai = ChatOpenAI(model="gpt-4.1")

    llm_azure = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )

    llm = llm_openai if backend == 1 else llm_azure
    print(f"Using backend: {'OpenAI' if backend == 1 else 'Azure OpenAI'}")

    ## 2. Setup multiple MCP servers
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
    agent = create_agent(model=llm, tools=tools)

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
    parser = argparse.ArgumentParser(description="LangChain MCP agent demo")
    parser.add_argument(
        "--backend", type=int, default=0,
        help="LLM backend: 0=Azure OpenAI (default), 1=OpenAI"
    )
    args = parser.parse_args()
    asyncio.run(test_function(backend=args.backend))


if __name__ == "__main__":
    main()
