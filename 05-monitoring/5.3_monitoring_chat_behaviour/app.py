from collections import deque
import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = deque()
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}

# Set up OpenAI API key


def get_response(message):
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
                                              messages=message,
                                              max_tokens=150)
    return response.choices[0].message.content.strip()


def clear_chat():
    st.session_state.messages.clear()
    st.session_state.feedback.clear()


st.title("Chat with LLM")

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    st.write(f"**{message['role']}:** {message['content']}")
    if message['role'] == 'assistant':
        col1, col2 = st.columns(2)
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
        st.session_state.messages.append(
            {'role': 'user', 'content': user_input})
        response = get_response(st.session_state.messages)
        st.session_state.messages.append(
            {'role': 'assistant', 'content': response})
        st.experimental_rerun()

# Clear chat button
if st.button("Clear Chat"):
    clear_chat()
    st.write("Chat cleared!")

# Display feedback (for debugging purposes)
st.write("### Feedback Data")
st.write(st.session_state.feedback)
