
import streamlit as st
from google import genai
from google.genai import types
import os

# Page configuration
st.set_page_config(
    page_title="CHABO AI",
    page_icon="🤖",
    layout="centered"
)

# Gemini API setup
API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not API_KEY:
    st.error("Gemini API key is missing. Please configure it.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Chatbot personality
SYSTEM_INSTRUCTION = """
You are CHABO AI, a helpful, friendly, and intelligent AI assistant.
You can answer questions about different topics.
Always provide clear, accurate, and easy-to-understand answers.
You can communicate in English, Filipino, and Cebuano.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Website design
st.title("🤖 CHABO AI")
st.caption("Your friendly AI assistant. Ask me anything!")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Message CHABO AI...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("CHABO AI is thinking..."):
            try:
                conversation = [
                    {
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [{"text": m["content"]}]
                    }
                    for m in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=conversation,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7
                    )
                )

                answer = response.text or "Sorry, I couldn't generate a response."
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Error: {e}")
