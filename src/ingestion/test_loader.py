from pdf_loader import load_pdf

pdf_path = "data/documents/design-patterns.pdf"

text = load_pdf(pdf_path)

print(text[:2000])