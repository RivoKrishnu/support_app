import streamlit as st
import google.generativeai as genai
import os
import re

# Using the streamlit-chat component for nicer chat bubbles
from streamlit_chat import message

# Load Gemini API key
api_key = "AIzaSyCwVh5ckIjNVOsgTirLX3rxV_EwOb0n_NU"

genai.configure(api_key=api_key)


# Crisis detection keywords and response message
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm",
    "can't go on", "hopeless", "worthless", "depressed", "panic attack"
]


CRISIS_MESSAGE = (
    "It sounds like you're going through a really tough time. "
    "Please consider reaching out for immediate support in India:\n\n"
    "• KIRAN Govt. Helpline: 1800-599-0019 (24/7, multi-language)\n"
    "• Vandrevala Foundation (call/WhatsApp): +91 9999666555 (24/7)\n"
    "• Tele MANAS: 14416 (24/7, 20+ languages)\n"
    "You are not alone, and help is available."  # option: add more if you wish
)


def check_for_crisis(text: str) -> bool:
    text = text.lower()
    for kw in CRISIS_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return True
    return False


def generate_response(chat_history: list) -> str:
    """
    Generate AI response using Gemini API.
    The prompt is constructed from the chat history.
    """
    prompt = (
        "You are a compassionate and empathetic mental health assistant. "
        "Provide supportive, non-judgmental, and helpful responses. "
        "Do not provide medical advice.\n\n"
    )

    for entry in chat_history:
        role, content = entry["role"], entry["content"]
        if role == "user":
            prompt += f"User: {content}\n"
        elif role == "assistant":
            prompt += f"Assistant: {content}\n"

    prompt += "Assistant:"

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I am having trouble right now. Please try again later. ({e})"


# Streamlit UI setup
st.set_page_config(page_title="Mental Health Chatbot (Gemini)", page_icon="💬")

st.title("💬 Mental Health Care Chatbot (Gemini)")
st.markdown(
    "Hello! I'm here to listen and provide supportive, empathetic responses. "
    "Please note this chatbot is not a replacement for professional help."
)

if "conversation" not in st.session_state:
    # Initialize with an empty conversation list of dicts {role:..., content:...}
    st.session_state.conversation = []

# Input form for user message
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    # Append user input to conversation history
    st.session_state.conversation.append({"role": "user", "content": user_input.strip()})

    # Check for crisis keywords
    if check_for_crisis(user_input):
        bot_reply = CRISIS_MESSAGE
    else:
        bot_reply = generate_response(st.session_state.conversation)

    # Append bot reply to conversation
    st.session_state.conversation.append({"role": "assistant", "content": bot_reply})

# Render all chat messages with streamlit-chat bubbles
for i, chat in enumerate(st.session_state.conversation):
    if chat["role"] == "user":
        message(chat["content"], is_user=True, key=f"user_{i}")
    else:
        message(chat["content"], is_user=False, key=f"bot_{i}")

# Footer disclaimer
st.markdown("---")
st.caption(
    "⚠️ This chatbot is for supportive conversation only and does not replace professional mental health care. In emergencies, contact crisis services immediately."
)
