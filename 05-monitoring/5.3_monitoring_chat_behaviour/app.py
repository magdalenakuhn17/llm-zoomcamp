from collections import deque
import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = deque()
if 'feedback' not in st.session_state:
    st.session_state.feedback = deque()

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

# Chat input
user_input = st.text_input("You:", key="input")
if st.button("Send"):
    if user_input:
        st.session_state.messages.append(
            {'role': 'user', 'content': user_input})
        response = get_response(st.session_state.messages)
        st.session_state.messages.append(
            {'role': 'assistant', 'content': response})

# Display chat history
for message in st.session_state.messages:
    st.write(f"**{message['role']}:** {message['content']}")

# Feedback input
st.write("### Give Feedback")
feedback_input = st.text_input("Feedback:", key="feedback_input")
if st.button("Submit Feedback"):
    if feedback_input:
        st.session_state.feedback.append(feedback_input)
        st.write("Feedback submitted!")

# Clear chat button
if st.button("Clear Chat"):
    clear_chat()
    st.write("Chat cleared!")
