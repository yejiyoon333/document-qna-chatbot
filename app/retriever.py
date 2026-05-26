from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


stored_chunks = []
vectorizer = None
tfidf_matrix = None


def index_chunks(chunks: list[str]):
    global stored_chunks, vectorizer, tfidf_matrix

    stored_chunks = chunks
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(chunks)


def search_chunks(question: str, top_k: int = 3):
    if vectorizer is None or tfidf_matrix is None:
        return []

    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, tfidf_matrix).flatten()

    top_indexes = similarities.argsort()[-top_k:][::-1]

    results = []

    for index in top_indexes:
        results.append({
            "chunk": stored_chunks[index],
            "score": float(similarities[index])
        })

    return results
