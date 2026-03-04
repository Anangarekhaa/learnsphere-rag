from huggingface_hub import InferenceClient
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN")
)

def normalize(vec):
    vec = np.array(vec)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


def get_embedding(text):
    embedding = client.feature_extraction(
        text,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    embedding = normalize(embedding)

    return embedding.tolist()


def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2))