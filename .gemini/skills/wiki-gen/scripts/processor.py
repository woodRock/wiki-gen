import os
import shutil
import json
import re
from pathlib import Path
import fitz  # PyMuPDF
from semanticscholar import SemanticScholar
from dotenv import load_dotenv

load_dotenv()

S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
sch = SemanticScholar(api_key=S2_API_KEY)

INGEST_DIR = Path("ingest")
PROCESSED_DIR = Path("processed")
DOCS_DIR = Path("wiki/docs")
JS_DIR = DOCS_DIR / "js"
PAPERS_META_FILE = JS_DIR / "papers_meta.js"
GLOSSARY_FILE = JS_DIR / "glossary.js"

def ensure_dirs():
    INGEST_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "assets").mkdir(exist_ok=True)
    JS_DIR.mkdir(exist_ok=True, parents=True)

def extract_raw_data(pdf_path):
    """Extracts text and reference mapping from PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        
        # Heuristic to find bibliography entries [1] Author, Title...
        # We look for [num] at the end of the document
        bib_matches = re.findall(r"\[(\d+)\]\s+([^\[\n]+(?:\n(?!!\[)\s+[^\[\n]+)*)", text)
        refs_map = {}
        for num, content in bib_matches:
            if int(num) < 200:
                refs_map[num] = content.replace("\n", " ").strip()
        
        return text, refs_map
    except Exception as e:
        print(f"Error extracting raw data: {e}")
        return "", {}

def get_paper_info(query):
    try:
        results = sch.search_paper(query, limit=1)
        if results:
            p = sch.get_paper(results[0].paperId)
            authors = ", ".join([a.name for a in p.authors[:3]])
            if len(p.authors) > 3: authors += " et al."
            return {
                "title": p.title,
                "authors": authors,
                "year": p.year,
                "venue": p.venue or "N/A",
                "cc": p.citationCount,
                "abstract": (p.abstract or "")[:400],
                "paperId": p.paperId
            }
    except: pass
    return None

def process_paper_with_llm(pdf_path, papers_meta, glossary):
    """
    Since I am the LLM, I will perform the high-quality parsing.
    But for the script, I will implement the logic that SHOULD be there.
    """
    print(f"Processing {pdf_path.name}...")
    raw_text, refs_map = extract_raw_data(pdf_path)
    
    # We use the filename or first lines to identify the paper
    title_guess = pdf_path.stem.replace("_", " ")
    paper_info = get_paper_info(title_guess)
    
    if not paper_info:
        # Try first lines
        lines = [l.strip() for l in raw_text.split("\n") if len(l.strip()) > 10]
        if lines:
            paper_info = get_paper_info(lines[0])
            
    if not paper_info:
        print(f"Could not identify paper: {pdf_path.name}")
        return False

    paper_id = paper_info["paperId"]
    
    # Cross-reference the bibliography
    citation_links = {}
    print(f"  Fetching metadata for {len(refs_map)} references...")
    for num, ref_text in list(refs_map.items())[:15]: # Limit to 15 for speed
        ref_info = get_paper_info(ref_text[:100])
        if ref_info:
            citation_links[num] = ref_info
            # Add to global papers_meta for hover cards
            papers_meta[ref_info["paperId"]] = ref_info

    # Now generate the Markdown content
    # In a real scenario, this would call an LLM API. 
    # Here, I (the Gemini agent) will generate it for this specific paper after the script runs
    # or I will make the script generate a placeholder that I then replace.
    
    generate_wikipedia_page(paper_info, raw_text, citation_links, pdf_path)
    
    papers_meta[paper_id] = paper_info
    shutil.move(str(pdf_path), str(PROCESSED_DIR / pdf_path.name))
    return True

def generate_wikipedia_page(info, text, citation_links, pdf_path):
    paper_id = info["paperId"]
    # For now, I'll write a "High Quality Placeholder" that I will fill in turn-by-turn
    # because I need to be the one doing the summarization.
    
    content = f"""# {info['title']}

<div class="paper-metadata">
**Authors:** {info['authors']}  
**Year:** {info['year']}  
**Venue:** {info['venue']}  
**Paper ID:** {paper_id}
</div>

> [!NOTE]
> This page is being generated in a high-quality Wikipedia style.

## Summary
(The LLM agent will populate this section with a detailed, structured summary including equations and figure references)

## Glossary
(The LLM agent will populate this section with technical terms and definitions)

## References
"""
    for num, ref in citation_links.items():
        content += f"[{num}] [{ref['title']}](./{ref['paperId']}.md)\n"
        
    with open(DOCS_DIR / f"{paper_id}.md", "w") as f:
        f.write(content)

def main():
    ensure_dirs()
    pdfs = list(INGEST_DIR.glob("*.pdf"))
    if not pdfs:
        print("No new PDFs in ingest/")
        return
    
    papers_meta = {}
    glossary = {}
    
    for pdf in pdfs:
        process_paper_with_llm(pdf, papers_meta, glossary)
    
    # Update papers_meta.js
    existing_meta = {}
    if PAPERS_META_FILE.exists():
        try:
            m = re.search(r"window\.PAPERS_META = (\{.*\});", PAPERS_META_FILE.read_text(), re.DOTALL)
            if m: existing_meta = json.loads(m.group(1))
        except: pass
    existing_meta.update(papers_meta)
    PAPERS_META_FILE.write_text(f"window.PAPERS_META = {json.dumps(existing_meta, indent=2)};\n")

if __name__ == "__main__":
    main()
