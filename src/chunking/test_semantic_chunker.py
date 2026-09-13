from ingestion.pdf_loader import load_pdf
from chunking.semantic_chunker import semantic_chunk

pdf_path = "data/documents/design-patterns.pdf"

text = load_pdf(pdf_path)
chunks = semantic_chunk(text)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])