from ingestion.pdf_loader import load_pdf
from chunking.simple_chunker import simple_chunk

pdf_path = "data/documents/design-patterns.pdf"

text = load_pdf(pdf_path)
chunks = simple_chunk(text)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])