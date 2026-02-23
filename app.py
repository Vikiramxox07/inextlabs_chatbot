import json
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="iNextLabs Support Bot")
st.set_page_config(page_title="iNextLabs Support Bot")
st.title("🤖 iNextLabs Customer Support Bot")
st.write("Powered by Google AI Studio (Gemini)")

st.divider()
st.subheader("SRE Test Section")

if st.button("Trigger SRE Failure"):
    raise Exception("SRE Test Failure")

@st.cache_data
def load_data():
    with open("support_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

faq_data = load_data()

def search_json(user_question):
    user_question = user_question.lower()

    for item in faq_data:
        for keyword in item["keywords"]:
            if keyword in user_question:
                return item["answer"]

    return None


def ask_gemini(question):
    try:
        context = "\n".join(
            [f"Q: {item['question']} A: {item['answer']}" for item in faq_data]
        )

        prompt = f"""
You are a customer support chatbot for iNextLabs.

Knowledge Base:
{context}

User Question:
{question}

Answer clearly and professionally.
"""
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return (
            "I am an iNextLabs support assistant. "
            "Please ask questions related to iNextLabs."
        )

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask a question about iNextLabs")

if st.button("Send") and user_input:
    answer = search_json(user_input)
    if not answer:
        answer = ask_gemini(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Bot", answer))

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")
