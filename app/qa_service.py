import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def generate_answer(question: str, retrieved_chunks: list[dict]) -> dict:
    if not retrieved_chunks:
        return {
            "answer": "No relevant information was found in the uploaded document.",
            "sources": []
        }

    sources = []

    for item in retrieved_chunks:
        cleaned_chunk = clean_text(item["chunk"])

        sources.append({
            "text": cleaned_chunk[:700],
            "score": item["score"]
        })

    answer = (
        "Based on the uploaded document, the most relevant information is: "
        + sources[0]["text"]
    )

    return {
        "answer": answer,
        "sources": sources
    }
