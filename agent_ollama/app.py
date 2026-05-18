import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import agent_app

st.set_page_config(page_title="Agent Ollama", page_icon="🤖")
st.title("🤖 Agent Ollama")
st.caption("Powered by Ollama + LangGraph · Tools: math, weather alerts, weather forecast")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Chat input
if prompt := st.chat_input("Ask me anything — e.g. 'Any weather alerts in TX?' or 'What is 12 * 7?'"):
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = agent_app.invoke({"messages": st.session_state.messages})
            reply = result["messages"][-1].content
        st.markdown(reply)

    st.session_state.messages.append(AIMessage(content=reply))
