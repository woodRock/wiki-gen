"""
Non-LLM paper fetching: Semantic Scholar metadata + figure/text extraction.
Outputs a JSON stub for Claude to fill in the analysis fields.

Usage:
    python3 scripts/fetch_paper.py ingest/vaswani2017attention.pdf
    python3 scripts/fetch_paper.py ingest/  # process all PDFs
"""

import json
import os
import re
import sys
from pathlib import Path

import fitz
import pdf2doi
from dotenv import load_dotenv
from semanticscholar import SemanticScholar

load_dotenv()

pdf2doi.config.set('verbose', False)

S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
sch = SemanticScholar(api_key=S2_API_KEY)

INGEST_DIR = Path("ingest")
ASSETS_DIR = Path("wiki/site/assets")
OUTPUT_DIR = Path("/tmp/wiki-gen")


def ensure_dirs():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_full_text(pdf_path, max_chars=30000):
    doc = fitz.open(str(pdf_path))
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text) >= max_chars:
            break
    doc.close()
    text = text.replace('\x00', '')
    text = "".join(ch for ch in text if ch.isprintable() or ch in '\n\r\t')
    return text[:max_chars]


def extract_title_from_pdf(pdf_path):
    doc = fitz.open(str(pdf_path))
    first_page = doc[0]
    text = first_page.get_text()
    doc.close()
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 10:
            return line
    return None


def extract_caption(page):
    text = page.get_text()
    lines = text.split('\n')
    for line in lines:
        match = re.search(r'(?:Figure|Fig\.)\s+(\d+)[.:\s-]+(.{20,300})', line, re.IGNORECASE)
        if match:
            caption_text = match.group(2).strip()
            return re.sub(r'\s+', ' ', caption_text)
    return ""


def extract_figures(pdf_path, paper_id):
    figures = []
    doc = fitz.open(str(pdf_path))
    seen_captions = set()

    for page_num, page in enumerate(doc):
        for img_idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            if not base_image:
                continue
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            if len(image_bytes) < 10000:
                continue

            caption = extract_caption(page)
            if caption and caption in seen_captions:
                continue
            if caption:
                seen_captions.add(caption)

            filename = f"{paper_id}_fig{len(figures) + 1}.{image_ext}"
            filepath = ASSETS_DIR / "figures" / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            figures.append({
                'filename': filename,
                'caption': caption,
                'page': page_num + 1,
                'index': len(figures) + 1
            })

    doc.close()
    return figures


def extract_arxiv_id(identifier):
    """Extract arXiv ID from a DOI like 10.48550/arxiv.1706.03762."""
    match = re.search(r'arxiv[./](\d{4}\.\d{4,5})', identifier, re.IGNORECASE)
    return match.group(1) if match else None


def lookup_semantic_scholar(pdf_path):
    """Try multiple strategies to find the paper on Semantic Scholar."""
    paper = None

    # Strategy 1: DOI from pdf2doi
    identifier = None
    try:
        results = pdf2doi.pdf2doi(str(pdf_path))
        identifier = results.get('identifier')
    except Exception as e:
        print(f"  pdf2doi failed: {str(e)[:60]}")

    if identifier:
        # Strategy 1a: arXiv ID (most reliable for preprints)
        arxiv_id = extract_arxiv_id(identifier)
        if arxiv_id:
            print(f"  Trying arXiv ID: {arxiv_id}")
            try:
                paper = sch.get_paper(f"arXiv:{arxiv_id}")
            except Exception as e:
                print(f"  arXiv lookup failed: {str(e)[:60]}")

        # Strategy 1b: Raw DOI
        if not paper and '/' in identifier:
            print(f"  Trying DOI: {identifier}")
            try:
                paper = sch.get_paper(identifier)
            except Exception as e:
                print(f"  DOI failed: {str(e)[:60]}")

    # Strategy 2: Title extracted from PDF
    # Skip short/garbage lines (license notices, headers) by requiring >= 5 words
    if not paper:
        pdf_title = extract_title_from_pdf(pdf_path)
        if pdf_title and len(pdf_title.split()) >= 5:
            print(f"  Searching by PDF title: {pdf_title[:60]}...")
            try:
                results = sch.search_paper(pdf_title, limit=3)
                if results:
                    paper = results[0]
                    print(f"  Found: {paper.title[:60]}...")
            except Exception as e:
                print(f"  Title search failed: {str(e)[:60]}")

    # Strategy 3: Filename-based search (last resort — can match wrong papers)
    if not paper:
        stem = Path(pdf_path).stem
        # Strip author+year prefix to get a more useful search query
        # e.g. "vaswani2017attention" -> "attention"
        query = re.sub(r'^[a-z]+\d{4}', '', stem).replace('_', ' ').strip() or stem
        print(f"  Searching by filename-derived query: {query}")
        try:
            results = sch.search_paper(query, limit=3)
            if results:
                paper = results[0]
                print(f"  Found: {paper.title[:60]}...")
        except Exception:
            pass

    return paper


def extract_tags(paper):
    tags = []
    text = f"{paper.title} {(paper.abstract or '')}".lower()
    topic_keywords = {
        'transformer': 'transformer',
        'attention': 'attention-mechanism',
        'quantization': 'quantization',
        'kv-cache': 'kv-cache',
        'llm': 'large-language-models',
        'language model': 'large-language-models',
        'self-supervised': 'self-supervised-learning',
        'jepa': 'jepa',
        'world model': 'world-models',
        'latent': 'latent-space',
        'embedding': 'embeddings',
        'vision': 'computer-vision',
        'image': 'computer-vision',
    }
    for keyword, tag in topic_keywords.items():
        if keyword in text:
            tags.append(tag)
    return list(set(tags))[:5]


def fetch_paper(pdf_path):
    pdf_path = Path(pdf_path)
    print(f"Fetching metadata for {pdf_path.name}...")

    paper = lookup_semantic_scholar(pdf_path)
    if not paper:
        print(f"  ERROR: Could not find on Semantic Scholar")
        return None

    paper_id = paper.paperId
    print(f"  Paper ID: {paper_id}")
    print(f"  Title: {paper.title}")

    print(f"  Extracting figures...")
    figures = extract_figures(pdf_path, paper_id)
    print(f"  Found {len(figures)} figures")

    print(f"  Extracting text...")
    pdf_text = extract_full_text(pdf_path)

    # Build references list
    references = []
    if paper.references:
        for ref in paper.references[:20]:
            try:
                references.append({
                    'cited_paper_id': ref.paperId,
                    'title': ref.title,
                    'authors': [a.name for a in ref.authors] if ref.authors else [],
                    'year': ref.year,
                    'venue': ref.venue,
                    'abstract': ref.abstract,
                    'citation_count': ref.citationCount if hasattr(ref, 'citationCount') else 0,
                })
            except Exception:
                pass

    stub = {
        # Semantic Scholar metadata
        'paper_id': paper_id,
        'title': paper.title,
        'authors': [a.name for a in paper.authors] if paper.authors else [],
        'year': paper.year,
        'venue': paper.venue or 'N/A',
        'doi': paper.externalIds.get('DOI', ''),
        'abstract': paper.abstract or 'No abstract available.',
        'tldr': paper.tldr['text'] if paper.tldr else 'N/A',
        'citation_count': paper.citationCount,
        'influential_citation_count': paper.influentialCitationCount,
        'pdf_filename': pdf_path.name,
        'tags': extract_tags(paper),
        # Extracted content for Claude to read
        'pdf_text': pdf_text,
        'figures': figures,
        'references': references,
        # LLM-generated fields — Claude fills these in
        'lead_paragraph': '',
        'sections': [],
        'concept_breakdown': [],
        'math_equations': [],
        'figure_explanations': [],
        'see_also': [],
        'glossary_terms': [],
        'infobox_data': {},
        'main_concept': '',
        'animation_path': None,
        'summary': [],
        'key_points': [],
    }

    output_path = OUTPUT_DIR / f"{paper_id}.fetch.json"
    with open(output_path, 'w') as f:
        json.dump(stub, f, indent=2)

    print(f"  Written to {output_path}")
    return str(output_path)


def main():
    ensure_dirs()

    if len(sys.argv) < 2:
        print("Usage: python3 scripts/fetch_paper.py <pdf_path_or_dir>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_dir():
        pdfs = list(target.glob("*.pdf"))
        if not pdfs:
            print(f"No PDFs found in {target}")
            sys.exit(0)
        print(f"Found {len(pdfs)} PDFs")
        for pdf in pdfs:
            result = fetch_paper(pdf)
            if result:
                print(f"OK: {result}")
            print()
    elif target.suffix == '.pdf':
        result = fetch_paper(target)
        if result:
            print(f"OK: {result}")
    else:
        print(f"Expected a .pdf file or directory, got: {target}")
        sys.exit(1)


if __name__ == "__main__":
    main()
