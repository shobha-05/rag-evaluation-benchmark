import json
import numpy as np

from retrieval.search import search
from retrieval.embedder import model


DATASET_PATH = "data/questions/rag_eval_dataset_interview.json"

# Thresholds for semantic similarity
CORRECT_THRESHOLD = 0.55
PARTIAL_THRESHOLD = 0.40


def load_questions():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def evaluate():
    questions = load_questions()

    correct = 0
    partial = 0
    incorrect = 0

    print(f"\nEvaluating {len(questions)} questions...\n")

    for item in questions:
        question = item["question"]
        expected_answer = item["expected_answer"]

        # Retrieve top 5 chunks
        results = search(question, top_k=5)
        retrieved_chunks = results["documents"][0]

        # Embed expected answer
        expected_embedding = model.encode(expected_answer)

        # Compare expected answer with every retrieved chunk
        similarities = []

        for chunk in retrieved_chunks:
            chunk_embedding = model.encode(chunk)

            score = cosine_similarity(
                expected_embedding,
                chunk_embedding
            )

            similarities.append(score)

        # Best matching retrieved chunk
        best_score = max(similarities)

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
        correct * 1.0 +
        partial * 0.5
    ) / total

    print("\n========== SEMANTIC BASELINE ==========")
    print(f"Total questions : {total}")
    print(f"Correct         : {correct}")
    print(f"Partial         : {partial}")
    print(f"Incorrect       : {incorrect}")
    print(f"Semantic Score  : {weighted_score:.2%}")
    print("========================================\n")


if __name__ == "__main__":
    evaluate()

