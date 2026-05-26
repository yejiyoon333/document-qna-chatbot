import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_summary_question(question: str) -> bool:
    question = question.lower()

    summary_keywords = [
        "what is this document about",
        "what is the document about",
        "summarize",
        "summary",
        "about"
    ]

    return any(keyword in question for keyword in summary_keywords)


def generate_summary_answer(all_chunks: list[str]) -> dict:
    if not all_chunks:
        return {
            "answer": "No document has been uploaded yet.",
            "sources": []
        }

    first_chunk = clean_text(all_chunks[0])

    answer = (
        "This document appears to be about: "
        + first_chunk[:500]
    )

    return {
        "answer": answer,
        "sources": [
            {
                "text": first_chunk[:700],
                "score": None
            }
        ]
    }


def generate_answer(question: str, retrieved_chunks: list[dict], all_chunks: list[str]) -> dict:
    if is_summary_question(question):
        return generate_summary_answer(all_chunks)

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
