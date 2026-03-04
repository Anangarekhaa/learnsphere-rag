import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def generate_answer(question: str, retrieved_chunks: list):
    context = "\n\n".join(
        [chunk.chunk_text for _, chunk in retrieved_chunks[:3]]
    )
    citation = retrieved_chunks[0][1].document.filename

    prompt = f"""
You are answering a vendor security questionnaire for LearnSphere.

Rules:
- Answer ONLY using the provided reference text.
- Do NOT repeat the question.
- Be concise.
- If answer is not supported by references, respond exactly:
Not found in references.

Question:
{question}

Reference Material:
{context}

Instructions:
- Provide a concise answer (2–4 sentences).
- Base the answer strictly on the reference text.
- End the answer with this citation exactly:

[{citation}]
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Answer strictly using provided context."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content