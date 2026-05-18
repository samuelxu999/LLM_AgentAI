# LangChain Agent with MCP Servers

A demo showing how to use a LangChain agent with multiple MCP (Model Context Protocol) servers — one running locally over `stdio` and one running remotely over HTTP.

Reference: [LangChain MCP Adapters](https://reference.langchain.com/python/langchain-mcp-adapters)

## Overview

The agent (`main.py`) connects to two MCP servers simultaneously and routes tool calls accordingly:

| Server | Transport | Tools |
|--------|-----------|-------|
| `math_server.py` | stdio (local process) | `add`, `multiply` |
| `weather_server.py` | HTTP (`localhost:8000`) | weather lookup |

The LLM backend is **OpenAI GPT-4.1** via `langchain[openai]`.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An OpenAI API key

## Project Structure

```
LangChain_MCP/
├── main.py            # LangChain agent entry point
├── math_server.py     # Local stdio MCP server (add, multiply)
├── weather_server.py  # HTTP MCP server (weather lookup)
├── pyproject.toml     # Project dependencies
└── .env               # API keys (not committed)
```

## Configuration

Create a `.env` file in this directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Install Dependencies

```bash
uv sync
```

## Run

### 1. Start the weather HTTP MCP server

```bash
uv run weather_server.py
```

This starts the weather server on `http://localhost:8000/mcp`.

### 2. Run the agent demo

In a separate terminal:

```bash
uv run main.py
```

The agent will:
1. Discover tools from both MCP servers
2. Answer a math query using the local `math_server` (`(13 + 5) × 12`)
3. Answer a weather query using the HTTP `weather_server` (weather in Houghton, MI)
