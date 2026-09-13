from retrieval.search import search

query = "What is the Strategy Pattern?"

results = search(query)

for i, document in enumerate(results["documents"][0]):
    print(f"\n--- Result {i + 1} ---")
    print(document[:500])