import os
import shutil
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from semanticscholar import SemanticScholar

# Marker v1.x imports
from marker.config.parser import ConfigParser
from marker.models import create_model_dict
from marker.output import save_output

load_dotenv()

S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
sch = SemanticScholar(api_key=S2_API_KEY)

INGEST_DIR = Path("ingest")
PROCESSED_DIR = Path("processed")
DOCS_DIR = Path("wiki/docs")
ASSETS_DIR = DOCS_DIR / "assets"

print("Loading Marker models (this may take a while)...")
# Initialize models and config once
MODELS = create_model_dict()
DEFAULT_KWARGS = {
    "output_format": "markdown",
}
CONFIG_PARSER = ConfigParser(DEFAULT_KWARGS)
CONVERTER_CLS = CONFIG_PARSER.get_converter_cls()
CONVERTER = CONVERTER_CLS(
    config=CONFIG_PARSER.generate_config_dict(),
    artifact_dict=MODELS,
    processor_list=CONFIG_PARSER.get_processors(),
    renderer=CONFIG_PARSER.get_renderer(),
    llm_service=CONFIG_PARSER.get_llm_service(),
)

def ensure_dirs():
    INGEST_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "js").mkdir(exist_ok=True)
    (DOCS_DIR / "css").mkdir(exist_ok=True)

def get_paper_metadata(identifier):
    try:
        if '/' in identifier: # DOI
            return sch.get_paper(identifier)
        else:
            results = sch.search_paper(identifier, limit=1)
            return results[0] if results else None
    except:
        return None

def process_pdf(pdf_path):
    print(f"Processing {pdf_path.name} with Marker v1.x...")
    try:
        # 1. Convert PDF using Marker
        rendered = CONVERTER(str(pdf_path))
        
        # 2. Get metadata from Semantic Scholar
        title_guess = rendered.metadata.get("title") or pdf_path.stem
        paper = get_paper_metadata(title_guess)
        
        if not paper:
            paper_id = pdf_path.stem
            display_title = title_guess
            authors = "Unknown"
            year = "N/A"
            abstract = ""
            venue = ""
            citation_count = 0
        else:
            paper_id = paper.paperId
            display_title = paper.title
            authors = ", ".join([a.name for a in paper.authors])
            year = paper.year
            abstract = paper.abstract or ""
            venue = paper.venue or ""
            citation_count = paper.citationCount

        # 3. Save output
        # Marker's save_output handles the markdown and images
        out_folder = DOCS_DIR
        base_filename = paper_id
        save_output(rendered, str(out_folder), base_filename)
        
        md_file_path = DOCS_DIR / f"{paper_id}.md"
        with open(md_file_path, "r") as f:
            full_content = f.read()
        
        # Prepend our header
        header = f"""# {display_title}

<div class="paper-metadata">
**Authors:** {authors} | **Year:** {year} | **Venue:** {venue}
**Citations:** {citation_count}
</div>

## Abstract
{abstract}

---

"""
        # Marker output might have its own title, we might want to clean it
        # but for now we just prepend.
        full_content = header + full_content
        
        with open(md_file_path, "w") as f:
            f.write(full_content)

        # 4. Update the papers_meta.js for hover cards
        meta_entry = {
            "title": display_title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "cc": citation_count,
            "abstract": (abstract[:300] + "...") if len(abstract) > 300 else abstract
        }
        
        meta_db_path = Path("wiki/papers_db.json")
        db = {}
        if meta_db_path.exists():
            with open(meta_db_path, "r") as f:
                db = json.load(f)
        db[paper_id] = meta_entry
        with open(meta_db_path, "w") as f:
            json.dump(db, f, indent=2)
            
        js_content = f"window.PAPERS_META = {json.dumps(db, indent=2)};"
        with open(DOCS_DIR / "js" / "papers_meta.js", "w") as f:
            f.write(js_content)

        # 5. Move PDF
        shutil.move(str(pdf_path), str(PROCESSED_DIR / pdf_path.name))
        
        update_index()
        return True
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_index():
    papers = []
    for file in DOCS_DIR.glob("*.md"):
        if file.name == "index.md":
            continue
        with open(file, "r") as f:
            line = f.readline()
            while line and not line.startswith("# "):
                line = f.readline()
            title = line.replace("# ", "").strip() if line else file.stem
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
