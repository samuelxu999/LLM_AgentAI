# LangChain Agent with MCP Servers

A demo showing how to use a LangChain agent with multiple MCP (Model Context Protocol) servers — one running locally over `stdio` and one running remotely over HTTP.

Reference: [LangChain MCP Adapters](https://reference.langchain.com/python/langchain-mcp-adapters)

## Overview

The agent (`main.py`) connects to two MCP servers simultaneously and routes tool calls accordingly:

| Server | Transport | Tools |
|--------|-----------|-------|
| `math_server.py` | stdio (local process) | `add`, `multiply` |
| `weather_server.py` | HTTP (`localhost:8000`) | weather lookup |

Two LLM backends are supported and can be swapped in `main.py`:

| Backend | Model | Variable |
|---------|-------|----------|
| OpenAI | `gpt-4.1` | `llm_openai` |
| Azure OpenAI | `gpt-4o` (configurable) | `llm_azure` ← default |

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An OpenAI API key **or** an Azure OpenAI deployment

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

Create a `.env` file in this directory with the keys for whichever backend(s) you use:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-resource>.api.cognitive.microsoft.com/
AZURE_OPENAI_API_KEY=your_azure_api_key_here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
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
# Azure OpenAI (default)
uv run main.py

# OpenAI
uv run main.py --backend 1
```

| `--backend` | LLM |
|-------------|-----|
| `0` | Azure OpenAI (default) |
| `1` | OpenAI |

The agent will:
1. Discover tools from both MCP servers
2. Answer a math query using the local `math_server` (`(13 + 5) × 12`)
3. Answer a weather query using the HTTP `weather_server` (weather in Houghton, MI)
