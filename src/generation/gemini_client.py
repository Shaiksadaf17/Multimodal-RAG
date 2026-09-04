import os
from google import genai


def create_gemini_client():
    """Create a Gemini API client using the environment API key."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
        )

    return genai.Client(api_key=api_key)


def generate_answer(question, context):
    """
    Generate an answer using Gemini based only on retrieved context.
    """

    client = create_gemini_client()

    prompt = f"""
You are a helpful document question-answering assistant.

Answer the user's question using ONLY the provided context.

If the answer is not contained in the context, say:
"I could not find the answer in the provided documents."

Do not invent information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text