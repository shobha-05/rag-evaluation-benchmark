def semantic_chunk(text: str, max_chars: int = 1500):
    paragraphs = [
        p.strip()
        for p in text.splitlines()
        if p.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 1 <= max_chars:
            current_chunk += paragraph + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = paragraph + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks