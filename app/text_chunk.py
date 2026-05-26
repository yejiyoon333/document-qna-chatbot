def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    text = " ".join(text.split())

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end < len(text):
            last_period = text.rfind(".", start, end)
            last_space = text.rfind(" ", start, end)

            if last_period > start:
                end = last_period + 1
            elif last_space > start:
                end = last_space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = max(end - overlap, end)

    return chunks
