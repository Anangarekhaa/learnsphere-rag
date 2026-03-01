from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def chunk_text(text: str, chunk_size=250, overlap=50, min_chunk_tokens=30):
    encoding = tokenizer(
        text,
        add_special_tokens=False,
        return_offsets_mapping=True
    )

    offsets = encoding["offset_mapping"]
    total_tokens = len(offsets)

    chunks = []
    start_token = 0

    while start_token < total_tokens:
        end_token = min(start_token + chunk_size, total_tokens)

      
        if end_token - start_token < min_chunk_tokens:
            break

        start_char = offsets[start_token][0]
        end_char = offsets[end_token - 1][1]

        chunk = text[start_char:end_char]

        
        if end_token < total_tokens:
            remaining_text = text[end_char:]
            period_index = remaining_text.find(".")
            if 0 <= period_index <= 200:  
                end_char += period_index + 1
                chunk = text[start_char:end_char]

        chunks.append(chunk.strip())

        start_token += chunk_size - overlap

    return chunks