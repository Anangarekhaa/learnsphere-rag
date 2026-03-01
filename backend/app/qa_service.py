from app.retrieval import retrieve_top_chunks
from app.generator import generate_answer
import numpy as np
from app.embeddings import get_embedding

THRESHOLD = 0.40


def compute_confidence(results):
    if not results:
        return "None"

    top_score = results[0][0]

    if top_score < THRESHOLD:
        return "None"

    if len(results) == 1:
        return "Medium"

    second_score = results[1][0]
    gap = top_score - second_score

    HIGH_GAP = 0.15
    MEDIUM_GAP = 0.08

    if gap >= HIGH_GAP:
        return "High"
    elif gap >= MEDIUM_GAP:
        return "Medium"
    else:
        return "Low"


def answer_question(question: str, user_id: str):
    results, top_score = retrieve_top_chunks(question,user_id)
  

    if results is None or top_score < THRESHOLD:
        return {
            "question": question,
            "answer": "Not found in references.",
            "confidence": "None",
            "citations": []
        }

    answer = generate_answer(question, results)

    
    if answer.strip().startswith("Not found"):
        return {
            "question": question,
            "answer": "Not found in references.",
            "confidence": "None",
            "citations": []
        }

    confidence = compute_confidence(results)

    top_chunk = results[0][1]
    filename = top_chunk.document.filename

    return {
        "question": question,
        "answer": f"{answer} [{filename}]",
        "confidence": confidence,
        "citations": [filename]
    }
