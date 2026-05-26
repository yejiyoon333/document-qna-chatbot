import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_llm_answer(question: str, sources: list[dict]) -> str:
    context = "\n\n".join([source["text"] for source in sources])

    if not context.strip():
        return "No relevant information was found in the uploaded document."

    prompt = f"""
You are a document Q&A assistant.

Answer the user's question using only the document context below.
If the answer is not in the context, say: "I don't know based on the uploaded document."

Question:
{question}

Document context:
{context}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
