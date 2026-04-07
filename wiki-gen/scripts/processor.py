import os
import shutil
import pdf2doi
from semanticscholar import SemanticScholar
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Silence pdf2doi output
pdf2doi.config.set('verbose', False)

S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
sch = SemanticScholar(api_key=S2_API_KEY)

INGEST_DIR = Path("ingest")
PROCESSED_DIR = Path("processed")
DOCS_DIR = Path("wiki/docs")

def ensure_dirs():
    INGEST_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "assets").mkdir(exist_ok=True)

def process_pdf(pdf_path):
    print(f"Processing {pdf_path.name}...")
    try:
        # Extract DOI or Title
        results = pdf2doi.pdf2doi(str(pdf_path))
        identifier = results.get('identifier')
        
        if not identifier:
            print(f"Could not find DOI for {pdf_path.name}. Searching by title...")
            # If no DOI, try to search by filename/extracted title
            # pdf2doi might have found a title
            identifier = results.get('title')
        
        if not identifier:
            print(f"Failed to identify {pdf_path.name}")
            return False

        # Get data from Semantic Scholar
        if results.get('identifier_type') == 'doi' or (identifier and '/' in identifier):
            paper = sch.get_paper(identifier)
        else:
            # Search by title
            search_results = sch.search_paper(identifier, limit=1)
            if not search_results:
                print(f"No paper found on Semantic Scholar for {identifier}")
                return False
            paper = search_results[0]

        generate_markdown(paper, pdf_path)
        
        # Move PDF to processed
        shutil.move(str(pdf_path), str(PROCESSED_DIR / pdf_path.name))
        return True
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")
        return False

def generate_markdown(paper, pdf_path):
    paper_id = paper.paperId
    filename = f"{paper_id}.md"
    
    authors = ", ".join([a.name for a in paper.authors]) if paper.authors else "Unknown"
    year = paper.year if paper.year else "N/A"
    abstract = paper.abstract if paper.abstract else "No abstract available."
    tldr = paper.tldr['text'] if paper.tldr else "N/A"
    venue = paper.venue if paper.venue else "N/A"
    
    content = f"""# {paper.title}

**Authors:** {authors}  
**Year:** {year}  
**Venue:** {venue}  
**DOI:** [{paper.externalIds.get('DOI', 'N/A')}](https://doi.org/{paper.externalIds.get('DOI', '')})

## TL;DR
{tldr}

## Abstract
{abstract}

## Citations
- **Total Citations:** {paper.citationCount}
- **Influential Citations:** {paper.influentialCitationCount}

## References
"""
    # Add references (top 10 for brevity in wiki)
    if paper.references:
        for ref in paper.references[:10]:
            ref_id = ref.paperId
            ref_title = ref.title
            if ref_id:
                content += f"- [{ref_title}](./{ref_id}.md)\n"
            else:
                content += f"- {ref_title}\n"
    else:
        content += "No references found.\n"

    content += f"\n\n--- \n*Generated from: {pdf_path.name}*"

    with open(DOCS_DIR / filename, "w") as f:
        f.write(content)
    
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
