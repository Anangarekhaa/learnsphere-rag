import re


def chunk_text(text: str, chunk_size=250, overlap=50, min_chunk_tokens=30):

    words = re.findall(r"\S+", text)
    total_tokens = len(words)

    chunks = []
    start = 0

    while start < total_tokens:

        end = min(start + chunk_size, total_tokens)

    
        if end - start < min_chunk_tokens:
            break

        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

       
        if end < total_tokens:
            remaining_words = words[end:end + 40]
            sentence_extension = " ".join(remaining_words)
            period_match = re.search(r"\.", sentence_extension)

            if period_match:
                extension_length = period_match.start()
                extra_words = sentence_extension[:extension_length].split()
                chunk += " " + " ".join(extra_words)

        chunks.append(chunk.strip())

        # Move window with overlap
        start += chunk_size - overlap

    return chunks