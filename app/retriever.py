from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


stored_chunks = []
current_document_name = None
vectorizer = None
tfidf_matrix = None


def index_chunks(chunks: list[str], document_name: str):
    global stored_chunks, current_document_name, vectorizer, tfidf_matrix

    stored_chunks = chunks
    current_document_name = document_name

    if not chunks:
        vectorizer = None
        tfidf_matrix = None
        return

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(chunks)


def search_chunks(question: str, top_k: int = 3, min_score: float = 0.01):
    if vectorizer is None or tfidf_matrix is None:
        return []

    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, tfidf_matrix).flatten()

    top_indexes = similarities.argsort()[-top_k:][::-1]

    results = []

    for index in top_indexes:
        score = float(similarities[index])

        if score >= min_score:
            results.append({
                "chunk": stored_chunks[index],
                "score": score
            })

    return results


def get_all_chunks():
    return stored_chunks


def get_index_status():
    return {
        "document_name": current_document_name,
        "indexed_chunk_count": len(stored_chunks),
        "is_index_ready": vectorizer is not None and tfidf_matrix is not None
    }
