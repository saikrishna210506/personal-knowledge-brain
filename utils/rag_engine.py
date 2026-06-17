import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_answer(question, context, chat_history, memory_text=""):

    prompt = f"""
You are an AI Knowledge Assistant.

Use the following priority:

1. Memory
2. Previous Conversation
3. Document Context

Rules:
- Use memory first.
- Use previous conversation.
- Use document context.
- Do not invent information.
- If information is unavailable, say:
"I couldn't find that information in the uploaded documents."
- Give concise answers.

Memory:
{memory_text}

Previous Conversation:
{chat_history}

Document Context:
{context}

Current Question:
{question}
"""

    try:

        response = model.generate_content(prompt)
        print(response)
        print(response.text)

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"