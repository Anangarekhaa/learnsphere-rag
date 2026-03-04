from app.retrieval import retrieve_top_chunks
from app.generator import generate_answer
import numpy as np
from app.embeddings import get_embedding

THRESHOLD = 0.40


HIGH_SCORE = 0.70
MEDIUM_SCORE = 0.50

HIGH_GAP = 0.10
MEDIUM_GAP = 0.05


def compute_confidence(results):
    if not results:
        return "None"

    scores = [r[0] for r in results]

    top_score = scores[0]

   
    if top_score < THRESHOLD:
        return "None"

    
    if len(scores) == 1:
        if top_score >= HIGH_SCORE:
            return "High"
        elif top_score >= MEDIUM_SCORE:
            return "Medium"
        else:
            return "Low"

    second_score = scores[1]
    gap = top_score - second_score

    
    if top_score >= HIGH_SCORE and gap >= MEDIUM_GAP:
        return "High"

   
    if top_score >= MEDIUM_SCORE:
        return "Medium"

   
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
