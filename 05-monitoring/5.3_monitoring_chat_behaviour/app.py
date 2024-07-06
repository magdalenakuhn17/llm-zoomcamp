import streamlit as st
from openai import OpenAI

client = OpenAI(api_key='your-openai-api-key')
from collections import deque

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = deque()
if 'feedback' not in st.session_state:
    st.session_state.feedback = deque()

# Set up OpenAI API key

def get_response(message):
    response = client.completions.create(engine="davinci-codex",
    prompt=message,
    max_tokens=150)
    return response.choices[0].text.strip()

def clear_chat():
    st.session_state.messages.clear()
    st.session_state.feedback.clear()

st.title("Chat with LLM")

# Chat input
user_input = st.text_input("You:", key="input")
if st.button("Send"):
    if user_input:
        st.session_state.messages.append(("User", user_input))
        response = get_response(user_input)
        st.session_state.messages.append(("LLM", response))

# Display chat history
for sender, msg in st.session_state.messages:
    st.write(f"**{sender}:** {msg}")

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
