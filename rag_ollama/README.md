# Local Chatbot-RAG with Ollama

A local Retrieval-Augmented Generation (RAG) chatbot system built with Ollama, ChromaDB, LangChain, and Streamlit. All models run locally — no cloud API required.

**References:**
- `rag_agent.py`: https://www.freecodecamp.org/news/build-a-local-ai/
- `app.py`: https://medium.com/@Shamimw/building-a-local-rag-based-chatbot-using-chromadb-langchain-and-streamlit-and-ollama-9410559c8a4d


## Project Structure

```
rag_ollama/
├── rag_agent.py       # Core RAG pipeline: load, embed, index, and query PDFs
├── rag_citation.py    # RAG with source document citations
├── app.py             # Streamlit chatbot web UI
├── data/              # Default folder for documents (e.g. test_doc.pdf)
├── pdf/               # Additional PDF documents
├── chroma_db/         # Persisted ChromaDB vector store (auto-created)
├── .env               # Environment variables (optional)
└── pyproject.toml     # Project dependencies
```


## Prerequisites

### 1. Install uv

Ensure `uv` is available on your local system:

- uv: https://docs.astral.sh/uv/getting-started/installation/

### 2. Install Ollama and pull models

Install Ollama from https://ollama.com, then pull the required models:

```bash
# Embedding model
ollama pull nomic-embed-text:v1.5

# LLM (default)
ollama pull qwen3:8b

# Optional: alternative LLM supported by the Streamlit app
ollama pull deepseek-r1:8b
```

### 3. Configure environment (optional)

Create a `.env` file to set a custom document directory:

```bash
DOC_DIRECTORY=/path/to/your/pdf/folder/
```


## Install Dependencies

```bash
uv add langchain langchain-community langchain-core langchain-ollama chromadb sentence-transformers pypdf python-dotenv tiktoken streamlit
```


## Usage

### rag_agent.py — Core RAG pipeline

```bash
# Show help
python rag_agent.py -h

# Demo: load, index, and query the default document (data/test_doc.pdf)
python rag_agent.py

# Add a document to the vector store (default: data/test_doc.pdf)
python rag_agent.py --test_func 1

# Add a specific document
python rag_agent.py --test_func 1 --doc_folder pdf/ --doc_name chapter1.pdf
```

| Argument | Default | Description |
|---|---|---|
| `--test_func` | `0` | `0` = demo case, `1` = add document to vector store |
| `--doc_folder` | `data/` | Folder containing the PDF |
| `--doc_name` | `test_doc.pdf` | PDF filename to load |

### rag_citation.py — RAG with source citations

Queries the vector store and prints the answer along with the source document and page number for each retrieved chunk.

```bash
python rag_citation.py
```

### app.py — Streamlit chatbot UI

```bash
streamlit run app.py
```

Open `http://127.0.0.1:8501` (or `http://<host_ip>:8501`) in a browser.

**Sidebar settings:**

| Setting | Options | Description |
|---|---|---|
| Model | `qwen3:8b`, `deepseek-r1:8b` | LLM to use for answering |
| Max History | 1–10 | Number of conversation turns to retain |
| Context Size | 1024–16384 | LLM context window in tokens |
| SSE Response | on/off | Stream the response character by character |
