import numpy as np
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_embedding(text):
    model = get_model()
    
    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=32
    )
    
    return [float(x) for x in embedding]


def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2))

