import streamlit as st
import google.generativeai as genai
import os
import re

# Load Gemini API key
api_key = "AIzaSyCwVh5ckIjNVOsgTirLX3rxV_EwOb0n_NU"
genai.configure(api_key=api_key)

# Basic crisis keyword list & message
CRISIS_KEYWORDS = ["suicide", "kill myself", "end my life", "self harm",
                   "can't go on", "hopeless", "worthless", "depressed", "panic attack"]
CRISIS_MESSAGE = (
    "It sounds like you're going through a really tough time. "
    "Please consider reaching out for immediate support:\n"
    "National Suicide Prevention Lifeline: 1-800-273-8255 (USA)\n"
    "Crisis Text Line: Text HOME to 741741 (USA)\n"
    "You are not alone, and help is available."
)

def check_for_crisis(text):
    text = text.lower()
    for kw in CRISIS_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return True
    return False

def generate_response(conversation_history):
    prompt = "You are a compassionate mental health assistant.\n"
    for line in conversation_history:
        prompt += line + "\n"
    prompt += "Assistant:"

    # Use an appropriate Gemini model name, adjust if needed
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.title("Mental Health Chatbot with Gemini API")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:")

if st.button("Send") and user_input.strip():
    st.session_state.history.append(f"User: {user_input}")

    if check_for_crisis(user_input):
        bot_response = CRISIS_MESSAGE
    else:
        bot_response = generate_response(st.session_state.history)

    st.session_state.history.append(f"Assistant: {bot_response}")

# Display conversation
for message in st.session_state.history:
    if message.startswith("User:"):
        st.markdown(f"**You:** {message[5:].strip()}")
    else:
        st.markdown(f"**Bot:** {message[10:].strip()}")
