from collections import deque
import streamlit as st
import os
import uuid
from openai import OpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Initialize session state variables
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}

# Set up chat history storage
chat_message_history = SQLChatMessageHistory(
    session_id=st.session_state.session_id,
    connection_string="sqlite:///sqlite.db"
)

# Define the prompt template and chain
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatOpenAI()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///sqlite.db"
    ),
    input_messages_key="question",
    history_messages_key="history",
)


def clear_chat():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.feedback.clear()
    # Reinitialize chat history with new session ID
    chat_message_history.session_id = st.session_state.session_id


st.title("Chat with LLM")

# Display session ID
st.write(f"**Session ID:** {st.session_state.session_id}")

# Display chat history
for idx, message in enumerate(chat_message_history.messages):
    if type(message) == HumanMessage:
        st.write(f"**User:** {message.content}")
    else:
        st.write(f"**AI:** {message.content}")
        col1, col2, _, _, _ = st.columns(5)
        with col1:
            if st.button("👍", key=f"thumbs_up_{idx}"):
                st.session_state.feedback[idx] = 'thumbs_up'
        with col2:
            if st.button("👎", key=f"thumbs_down_{idx}"):
                st.session_state.feedback[idx] = 'thumbs_down'

# Chat input
user_input = st.text_input("You:", key="input")
if st.button("Send"):
    if user_input:
        response = chain_with_history.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": st.session_state.session_id}}
        )
        st.experimental_rerun()

# Clear chat button
if st.button("Clear Chat"):
    clear_chat()
    st.experimental_rerun()

# Display feedback (for debugging purposes)
st.write("### Feedback Data")
st.write(st.session_state.feedback)
