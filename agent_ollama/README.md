# Simple AI Agent using LangGraph and Ollama

A demo project showing how to build a LangGraph agent with a local Ollama model and multiple tools, including math operations and live weather data from the National Weather Service (NWS) API. Includes both a CLI demo and a Streamlit web UI.

## Prerequisites

- [Ollama](https://ollama.com) running locally with the `qwen3:8b` model pulled:
  ```bash
  ollama pull qwen3:8b
  ```
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed on your system.

## Install dependencies

```bash
uv add langchain-ollama langgraph streamlit
```

## Project structure

```
agent_ollama/
├── models.py   # Ollama model setup and tool binding
├── tools.py    # Tool definitions (math, weather alerts, weather forecast)
├── agent.py    # LangGraph agent workflow
├── main.py     # CLI demo examples
└── app.py      # Streamlit web UI
```

## Available tools

| Tool | Description |
|---|---|
| `add(a, b)` | Adds two numbers |
| `multiply(a, b)` | Multiplies two numbers |
| `get_coordinates(location)` | Geocodes a place name to latitude/longitude (via OpenStreetMap Nominatim) |
| `get_weather_alerts(state)` | Active NWS alerts for a US state (e.g. `"CA"`) |
| `get_weather_forecast(latitude, longitude)` | NWS forecast for a lat/lon location |

Weather data is fetched live from `https://api.weather.gov` (US locations only). The agent automatically chains `get_coordinates` → `get_weather_forecast` when given a place name.

## Run the CLI demo

```bash
uv run main.py
```

This runs three examples: a math query, weather alerts for California, and a weather forecast for New York City.

## Run the web UI

```bash
uv run streamlit run app.py --server.port 8080
```

Then open **http://localhost:8080** in your browser. Type any question in the chat input — the agent will automatically pick the right tool(s) to answer. Press `Ctrl+C` to stop the server.

Example prompts:
- `Are there any active weather alerts in TX?`
- `What is the weather forecast for latitude 47.61 and longitude -122.33?`
- `What is the weather forecast for Hopughton, Mi?`
- `What is (15 + 3) * 4?`
