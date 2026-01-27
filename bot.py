import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

with open("support_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

def search_faq(question):
    for item in faq_data:
        if item["question"].lower() in question.lower():
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
            "Please ask questions related to iNextLabs or enterprise AI solutions."
        )

def chatbot():
    print("iNextLabs Gemini Support Bot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        answer = search_faq(user_input)
        if answer:
            print("Bot:", answer)
        else:
            print("Bot:", ask_gemini(user_input))

chatbot()
