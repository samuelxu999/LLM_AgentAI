# Chatbot using Flask and Ollama

A demo project showing how to build a simple web-based chatbot using [Flask](https://flask.palletsprojects.com/) and a local [Ollama](https://ollama.com) model. The backend exposes a REST API that the browser-based chat UI calls in real time.

## Prerequisites

- [Ollama](https://ollama.com) running locally with the `deepseek-r1:8b` model pulled:
  ```bash
  ollama pull deepseek-r1:8b
  ```
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or `pip`

### Optional: manage Ollama models via Open WebUI

```bash
## Start Open WebUI docker instance
docker run -d --rm --network=host -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --name open-webui ghcr.io/open-webui/open-webui:main

## Check running containers
docker container ps

## Stop Open WebUI
docker container stop open-webui
```

## Project structure

```
chatbot_ollama/
├── main.py               # Flask app — routes and Ollama async client
├── templates/
│   └── chatbot.html      # Chat UI template
├── static/
│   ├── chatscript.js     # Frontend chat logic
│   └── index.css         # Styles
├── system.txt            # System prompt (optional)
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

Open **http://127.0.0.1:8000** (or `http://<host_ip>:8000`) in a web browser and start chatting.
