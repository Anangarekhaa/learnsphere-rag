from sqlalchemy.orm import joinedload
from app.models import Document, DocumentChunk
from app.embeddings import get_embedding, cosine_similarity
from app.database import SessionLocal


def retrieve_top_chunks(query: str, user_id, top_k: int = 5):
    session = SessionLocal()

    query_embedding = get_embedding(query)

    chunks = (
        session.query(DocumentChunk)
        .join(Document)  # join to access user_id
        .options(joinedload(DocumentChunk.document))
        .filter(Document.user_id == user_id)   
        .all()
    )

    if not chunks:
        session.close()
        return [], 0

    scored_chunks = []

    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk.embedding)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    top_results = scored_chunks[:top_k]
    top_score = top_results[0][0] if top_results else 0

    session.close()

    return top_results, top_score