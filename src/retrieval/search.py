from retrieval.vector_store import collection
from retrieval.embedder import model


def search(query: str, top_k: int = 5):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results