from langchain_ollama import ChatOllama

from tools import *

# Bind tools to the local model
llm_model = ChatOllama(model="qwen3:8b", temperature=0)
llm_with_tools = llm_model.bind_tools(tools)
