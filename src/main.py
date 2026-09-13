from ingestion.pdf_loader import load_pdf
from chunking.simple_chunker import simple_chunk
from retrieval.embedder import create_embeddings
from retrieval.vector_store import store_chunks


pdf_path = "data/documents/design-patterns.pdf"

text = load_pdf(pdf_path)
chunks = simple_chunk(text)

print(f"Created {len(chunks)} chunks")

embeddings = create_embeddings(chunks)

print("Created embeddings")

store_chunks(chunks, embeddings)

print("Stored chunks in ChromaDB")