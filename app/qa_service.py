import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_sources(retrieved_chunks: list[dict], all_chunks: list[str]) -> list[dict]:
    sources = []

    for item in retrieved_chunks:
        cleaned_chunk = clean_text(item["chunk"])

        sources.append({
            "text": cleaned_chunk[:800],
            "score": round(item["score"], 4)
        })

    if not sources and all_chunks:
        fallback_text = clean_text(" ".join(all_chunks[:2]))

        sources.append({
            "text": fallback_text[:1200],
            "score": None
        })

    return sources
