from app.database import SessionLocal
from app.models import Document, DocumentChunk
from app.chunking import chunk_text
from app.embeddings import get_embedding
import os

session = SessionLocal()

folder_path = "sample_data/reference_documents"

for filename in os.listdir(folder_path):
    if not filename.endswith(".txt"):
        continue

    with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
        content = f.read()

    # Save document
    doc = Document(filename=filename, content=content)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    # Chunk
    chunks = chunk_text(content)

    for chunk in chunks:
        embedding = get_embedding(chunk)

        chunk_obj = DocumentChunk(
            document_id=doc.id,
            chunk_text=chunk,
            embedding=embedding.tolist()  
        )

        session.add(chunk_obj)

    session.commit()

session.close()

print("Ingestion complete.")

