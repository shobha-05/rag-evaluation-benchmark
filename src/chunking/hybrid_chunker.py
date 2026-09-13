def hybrid_chunk(text: str, max_chars: int = 1000):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 <= max_chars:
            current += line + " "
        else:
            if current:
                chunks.append(current.strip())

            current = line + " "

    if current:
        chunks.append(current.strip())

    return chunks