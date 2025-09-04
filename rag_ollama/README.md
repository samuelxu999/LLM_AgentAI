# Build local Chatbot-RAG

This project provides a simple demo of local RAG chatbot system by using Ollama, ChromaDB, LangChain, and Streamlit.

rag_agent.py, reference: https://www.freecodecamp.org/news/build-a-local-ai/

app.py reference: https://medium.com/@Shamimw/building-a-local-rag-based-chatbot-using-chromadb-langchain-and-streamlit-and-ollama-9410559c8a4d


## Install uv.

Ensure `uv` are ready on you local system.

Here are official installation guideline:

- uv: https://docs.astral.sh/uv/getting-started/installation/


## Install Dependencies
```bash
uv add langchain langchain-community langchain-core langchain-ollama chromadb sentence-transformers pypdf python-dotenv tiktoken streamlit
```

## Ensure you have installed ollama and deploy models

Pull and Run Qwen 3 with Ollama
```bash
ollama pull qwen3:8b
```

## Run the rag_agent: 0 - demo case; 1 - add doc to vector database
```bash
python rag_agent.py -h // get help

python rag_agent.py // run demo case

python rag_agent.py --test_func 1 // run add_document(), use default: data/test_doc.pdf

python rag_agent.py --test_func 1 --doc_folder df_book --doc_name chapter1.pdf //
```

## Run the Streamlit App to launch chatbot
```bash
streamlit run app.py
```

## Open chatbot GUI page
Input "http://127.0.0.1:8501" (or http://host_ip:8501) in address bar of webbrowser