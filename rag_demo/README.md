# A simple RAG Demo

This project provides an overview RAG operations in terms of split, chunking, embedding, indexing, re-ranking, retrieve, etc.

You can use jupyter lab to execute code and learn key steps and functions in RAG.

Here is reference: https://github.com/MarkTechStation/VideoCode/tree/main/%E4%BD%BF%E7%94%A8Python%E6%9E%84%E5%BB%BARAG%E7%B3%BB%E7%BB%9F/rag

## Install uv and Jupyter.

Ensure `uv` and `Jupyter` are ready on you local system.

Here are official installation guideline:

- uv: https://docs.astral.sh/uv/getting-started/installation/
- Jupyter: https://jupyter.org/install

## Add your API Key.
Open `.env` file and then add you API key

```.env
GEMINI_API_KEY=@user_key.
```

Replace @user_key with your Google Gemini API KEY.

You can get a key via https://aistudio.google.com/apikey.

## Install Dependencies
```bash
uv add sentence_transformers chromadb google-genai python-dotenv
```

## Using `uv` launch Jupyter Notebook：

```bash
uv run --with jupyter jupyter lab
```

