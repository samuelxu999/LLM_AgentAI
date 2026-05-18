from langchain_core.messages import HumanMessage
from agent import *

def math_example():
    inputs = {"messages": [HumanMessage(content="What is (15 + 3) * 4?")]}
    result = app.invoke(inputs)
    print(result["messages"][-1].content)


def weather_example():
    # Example 1: get active weather alerts for California
    inputs = {"messages": [HumanMessage(content="Are there any active weather alerts in CA?")]}
    result = app.invoke(inputs)
    print("=== Weather Alerts ===")
    print(result["messages"][-1].content)

    # Example 2: get weather forecast for New York City (lat/lon)
    inputs = {"messages": [HumanMessage(
        content="What is the weather forecast for latitude 40.71 and longitude -74.01?"
    )]}
    result = app.invoke(inputs)
    print("\n=== Weather Forecast ===")
    print(result["messages"][-1].content)

    # Example 2: get weather forecast for New York City (lat/lon)
    inputs = {"messages": [HumanMessage(
        content="How about the latest weather in Houghton, MI?"
    )]}
    result = app.invoke(inputs)
    print("\n=== Weather Forecast ===")
    print(result["messages"][-1].content)

def demo_case():
    math_example()
    weather_example()


if __name__ == "__main__":
    demo_case()

