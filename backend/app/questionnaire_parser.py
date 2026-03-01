import re
import os
from app.file_utils import extract_text_from_pdf


def parse_questionnaire(file_path: str):
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".pdf":
        content = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    content = content.strip()

    # Split by blank lines first
    blocks = re.split(r"\n\s*\n", content)

    # Fallback to numbered split
    if len(blocks) == 1:
        blocks = re.split(r"\n(?=\d+[\.\)])", content)

    questions = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        cleaned = re.sub(r"^(Q?\d+[\.\):]?\s*)", "", block, flags=re.IGNORECASE)
        questions.append(cleaned.strip())

    return questions