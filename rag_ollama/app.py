import streamlit as st

from langchain.memory import ConversationBufferMemory

from rag_agent import *

# ---- Streamlit UI ---- #
st.set_page_config(layout="wide")
st.title("Local Chatbot-RAG")

st.sidebar.header("Settings")
MODEL = st.sidebar.selectbox("Choose a Model", ["qwen3:8b", "deepseek-r1:7b"], index=0)
MAX_HISTORY = st.sidebar.number_input("Max History", 1, 10, 2)
CONTEXT_SIZE = st.sidebar.number_input("Context Size", 1024, 16384, 8192, step=1024)

# ---- Session State Setup ---- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "memory" not in st.session_state or st.session_state.get("prev_context_size") != CONTEXT_SIZE:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
    st.session_state.prev_context_size = CONTEXT_SIZE

# ---- LangChain Components ---- #

# 1. Get Embedding Function
embedding_function = get_embedding_function() # Using Ollama nomic-embed-text

# 2. To load existing DB:
vector_store = get_vector_store(embedding_function)

# 5. Create RAG Chain
rag_chain = create_rag_chain(vector_store, llm_model_name=MODEL)

# ---- Display Chat History ---- #
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---- Trim Chat Memory ---- #
def trim_memory():
    while len(st.session_state.chat_history) > MAX_HISTORY * 2:
        st.session_state.chat_history.pop(0)  # Remove oldest messages

# ---- Handle User Input ---- #
if prompt := st.chat_input("Say something"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    trim_memory()

    with st.chat_message("assistant"):
        response_container = st.empty()

        # Retrieve relevant documents based on user query
        response = rag_chain.invoke(prompt)

        response_container.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        trim_memory()
