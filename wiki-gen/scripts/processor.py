import os
import shutil
import pdf2doi
import fitz  # PyMuPDF
from semanticscholar import SemanticScholar
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv()

# Silence pdf2doi output
pdf2doi.config.set('verbose', False)

S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
sch = SemanticScholar(api_key=S2_API_KEY)

INGEST_DIR = Path("ingest")
PROCESSED_DIR = Path("processed")
DOCS_DIR = Path("wiki/docs")
ASSETS_DIR = DOCS_DIR / "assets"

def ensure_dirs():
    INGEST_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)

def extract_content(pdf_path, paper_id):
    doc = fitz.open(pdf_path)
    full_text = ""
    paper_assets_dir = ASSETS_DIR / paper_id
    paper_assets_dir.mkdir(exist_ok=True)
    
    img_count = 0
    for i in range(len(doc)):
        page = doc.load_page(i)
        
        # Extract text
        text = page.get_text("text")
        full_text += f"\n\n### Page {i+1}\n\n" + text
        
        # Extract images
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            img_filename = f"fig_{i+1}_{img_index}.{image_ext}"
            with open(paper_assets_dir / img_filename, "wb") as f:
                f.write(image_bytes)
            
            # Insert image reference in text
            # We use a path relative to the .md file in docs/
            full_text += f"\n\n![Figure {img_count+1}](./assets/{paper_id}/{img_filename})\n\n"
            img_count += 1
            
    return full_text

def process_pdf(pdf_path):
    print(f"Processing {pdf_path.name}...")
    try:
        results = pdf2doi.pdf2doi(str(pdf_path))
        identifier = results.get('identifier')
        
        if not identifier:
            identifier = results.get('title')
        
        if not identifier:
            print(f"Failed to identify {pdf_path.name}")
            return False

        if results.get('identifier_type') == 'doi' or (identifier and '/' in identifier):
            paper = sch.get_paper(identifier)
        else:
            search_results = sch.search_paper(identifier, limit=1)
            if not search_results:
                print(f"No paper found on Semantic Scholar for {identifier}")
                return False
            paper = search_results[0]

        paper_id = paper.paperId
        full_content = extract_content(pdf_path, paper_id)
        generate_markdown(paper, pdf_path, full_content)
        
        shutil.move(str(pdf_path), str(PROCESSED_DIR / pdf_path.name))
        return True
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")
        return False

def generate_markdown(paper, pdf_path, full_content):
    paper_id = paper.paperId
    filename = f"{paper_id}.md"
    
    authors = ", ".join([a.name for a in paper.authors]) if paper.authors else "Unknown"
    year = paper.year if paper.year else "N/A"
    tldr = paper.tldr['text'] if paper.tldr else "N/A"
    
    header = f"""# {paper.title}

**Authors:** {authors} | **Year:** {year} | **DOI:** [{paper.externalIds.get('DOI', 'N/A')}](https://doi.org/{paper.externalIds.get('DOI', '')})

## Summary (TL;DR)
{tldr}

---

## Full Paper Content

{full_content}

---

## Metadata & References
- **Citations:** {paper.citationCount}
"""
    if paper.references:
        header += "\n### References\n"
        for ref in paper.references[:15]:
            ref_id = ref.paperId
            if ref_id:
                header += f"- [{ref.title}](./{ref_id}.md)\n"
            else:
                header += f"- {ref.title}\n"

    with open(DOCS_DIR / filename, "w") as f:
        f.write(header)
    
    update_index()

def update_index():
    papers = []
    for file in DOCS_DIR.glob("*.md"):
        if file.name == "index.md":
            continue
        with open(file, "r") as f:
            first_line = f.readline().strip()
            title = first_line.replace("# ", "")
            papers.append((title, file.name))
    
    index_content = "# Research Paper Wiki\n\nWelcome to your personalized research wiki.\n\n## Papers\n"
    for title, fname in sorted(papers):
        index_content += f"- [{title}](./{fname})\n"
    
    with open(DOCS_DIR / "index.md", "w") as f:
        f.write(index_content)

def main():
    ensure_dirs()
    pdfs = list(INGEST_DIR.glob("*.pdf"))
    if not pdfs:
        print("No new PDFs found in ingest/")
        return
    
    for pdf in pdfs:
        process_pdf(pdf)

if __name__ == "__main__":
    main()
