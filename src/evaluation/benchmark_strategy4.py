import json
import numpy as np
import chromadb

from ingestion.pdf_loader import load_pdf
from chunking.hybrid_chunker import hybrid_chunk
from retrieval.embedder import model

PDF_PATH = "data/documents/design-patterns.pdf"
DATASET_PATH = "data/questions/rag_eval_dataset_interview.json"

CORRECT_THRESHOLD = 0.55
PARTIAL_THRESHOLD = 0.40


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def build_collection():
    text = load_pdf(PDF_PATH)
    chunks = hybrid_chunk(text)

    print(f"Created {len(chunks)} hybrid chunks")

    embeddings = model.encode(chunks).tolist()

    client = chromadb.PersistentClient(
        path="data/chroma_strategy4"
    )

    collection = client.get_or_create_collection(
        name="design_patterns_hybrid"
    )

    if collection.count() == 0:
        for i, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            collection.add(
                ids=[str(i)],
                documents=[chunk],
                embeddings=[embedding],
            )

    print("Stored Strategy #4 chunks")

    return collection


def evaluate(collection):
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    correct = 0
    partial = 0
    incorrect = 0

    print(f"\nEvaluating {len(questions)} questions...\n")

    for item in questions:
        query_embedding = model.encode(
            item["question"]
        ).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
        )

        retrieved_chunks = results["documents"][0]

        expected_embedding = model.encode(
            item["expected_answer"]
        )

        scores = []

        for chunk in retrieved_chunks:
            chunk_embedding = model.encode(chunk)

            scores.append(
                cosine_similarity(
                    expected_embedding,
                    chunk_embedding
                )
            )

        best_score = max(scores)

        if best_score >= CORRECT_THRESHOLD:
            correct += 1
            result = "CORRECT"
        elif best_score >= PARTIAL_THRESHOLD:
            partial += 1
            result = "PARTIAL"
        else:
            incorrect += 1
            result = "INCORRECT"

        print(
            f"{item['question_id']} | "
            f"{result:9} | "
            f"score={best_score:.3f}"
        )

    total = len(questions)

    weighted_score = (
        correct + partial * 0.5
    ) / total

    print("\n========== STRATEGY #4 ==========")
    print(f"Total questions : {total}")
    print(f"Correct         : {correct}")
    print(f"Partial         : {partial}")
    print(f"Incorrect       : {incorrect}")
    print(f"Semantic Score  : {weighted_score:.2%}")
    print("=================================\n")


if __name__ == "__main__":
    collection = build_collection()
    evaluate(collection)