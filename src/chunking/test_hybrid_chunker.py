from ingestion.pdf_loader import load_pdf
from chunking.hybrid_chunker import hybrid_chunk

text = load_pdf("data/documents/design-patterns.pdf")
chunks = hybrid_chunk(text)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])