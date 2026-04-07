import fitz
import sys

def extract_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += f"## Page {page.number + 1}\n\n"
        text += page.get_text()
        text += "\n\n"
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_pymupdf.py <pdf_path>")
        sys.exit(1)
    
    content = extract_pdf(sys.argv[1])
    print(content[:1000])
