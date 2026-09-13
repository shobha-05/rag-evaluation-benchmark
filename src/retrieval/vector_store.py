import chromadb


client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(
    name="design_patterns"
)


def store_chunks(chunks, embeddings):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embedding],
        )