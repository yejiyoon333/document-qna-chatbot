import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_context_sources(retrieved_chunks: list[dict], all_chunks: list[str]) -> list[dict]:
    sources = []

    for item in retrieved_chunks:
        cleaned_chunk = clean_text(item["chunk"])

        sources.append({
            "text": cleaned_chunk[:1200],
            "score": round(item["score"], 4)
        })

    if not sources and all_chunks:
        fallback_text = clean_text(" ".join(all_chunks[:2]))

        sources.append({
            "text": fallback_text[:1500],
            "score": None
        })

    return sources


def build_display_sources(context_sources: list[dict]) -> list[dict]:
    display_sources = []

    for source in context_sources:
        display_sources.append({
            "preview": source["text"][:300],
            "score": source["score"]
        })

    return display_sources
