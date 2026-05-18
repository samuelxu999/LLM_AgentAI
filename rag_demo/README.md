# A Simple RAG Demo

A step-by-step Jupyter notebook demonstrating how to build a Retrieval-Augmented Generation (RAG) pipeline from scratch, covering splitting, chunking, embedding, vector storage, retrieval, reranking, and answer generation.

Reference: [Python RAG System by MarkTechStation](https://github.com/MarkTechStation/VideoCode/tree/main/%E4%BD%BF%E7%94%A8Python%E6%9E%84%E5%BB%BARAG%E7%B3%BB%E7%BB%9F/rag)

## Pipeline Overview

The notebook (`main.ipynb`) walks through 7 stages:

| Step | Description |
|------|-------------|
| 1 | **Split & chunk** — split a markdown document into text chunks |
| 2 | **Embedding model setup** — load `all-mpnet-base-v2` via `sentence-transformers` |
| 3 | **Embed chunks** — encode all chunks into dense vectors |
| 4 | **Vector store** — index embeddings in ChromaDB (`EphemeralClient`) |
| 5 | **Retrieve** — query the vector store for the top-k most relevant chunks |
| 6 | **Rerank** — refine results with `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` |
| 7 | **Generate** — feed reranked chunks and the query to **Gemini 2.5 Flash** for the final answer |

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or `pip`
- [Jupyter](https://jupyter.org/install)
- A Google Gemini API key — get one at <https://aistudio.google.com/apikey>

## Project Structure

```
rag_demo/
├── main.ipynb       # RAG pipeline notebook (7 steps)
├── doc_demo.md      # Sample knowledge-base document
├── pyproject.toml   # uv/PEP 517 project config
└── .env             # API keys (not committed)
```

## Configuration

Create a `.env` file in this directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_key_here
```

## Install Dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install chromadb google-genai python-dotenv sentence-transformers
```

## Run the Notebook

```bash
uv run --with jupyter jupyter lab
```

Then open `main.ipynb` and run the cells in order.
