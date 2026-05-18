# Chatbot Demo using Flask and Azure OpenAI

A demo project showing how to build a simple web-based chatbot using [Flask](https://flask.palletsprojects.com/) and [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service). The backend exposes a REST API that the browser-based chat UI calls in real time.

## Prerequisites

- An [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) resource with a deployed chat model (e.g. `gpt-4o`)
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or `pip`

## Environment variables

Create a `.env` file in the project root with your Azure OpenAI credentials:

```ini
AZURE_OAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OAI_KEY=<your-api-key>
AZURE_OAI_DEPLOYMENT=<your-deployment-name>
```

## Project structure

```
chatbot_demo/
├── main.py               # Flask app — routes and Azure OpenAI async client
├── system.txt            # System prompt sent to the model on every request
├── templates/
│   └── chatbot.html      # Chat UI template
├── static/
│   ├── chatscript.js     # Frontend chat logic
│   └── index.css         # Styles
├── requirements.txt      # pip dependencies
└── pyproject.toml        # uv/PEP 517 project config
```

## Install dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the chatbot web service

**Using uv:**
```bash
uv run main.py
```

**Using pip:**
```bash
python main.py
```

## Open the chatbot UI

Open **http://127.0.0.1:8080** (or `http://<host_ip>:8080`) in a web browser and start chatting.
