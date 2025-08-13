from langchain.chains import RetrievalQA

from rag_agent import *

# 1. Get Embedding Function
embedding_function = get_embedding_function() # Using Ollama nomic-embed-text

# 2. To load existing DB:
vector_store = get_vector_store(embedding_function)

# 3. Setup RAG chain with source retrieval
# llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    # Initialize the LLM
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0, # Lower temperature for more factual RAG answers
    num_ctx=4906 # IMPORTANT: Set context window size
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    # retriever=vector_store.as_retriever(),
        # Create the retriever
    retriever = vector_store.as_retriever(
        search_type="similarity", # Or "mmr"
        search_kwargs={'k': 3} # Retrieve top 3 relevant chunks
    ),
    return_source_documents=True # Important for citations
)

# 4. Query and get response with sources
query = "What is holochain?"
result = qa_chain({"query": query})

print("Answer:", result["result"])
print("\nSources:")
for doc in result["source_documents"]:
    # Access metadata for citation details
    print(f"  - Document: {doc.metadata['source']}, Page: {doc.metadata['page']}")