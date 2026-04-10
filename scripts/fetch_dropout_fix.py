import json
import sys
from semanticscholar import SemanticScholar
from pathlib import Path
import fitz
import re

sch = SemanticScholar()
paper_id = "34f25a8704614163c4095b3ee2fc969b60de4698"
pdf_path = Path("ingest/srivastava2013dropout.pdf")
ASSETS_DIR = Path("wiki/site/assets")

print(f"Fetching metadata for paper ID: {paper_id}")
paper = sch.get_paper(paper_id)

def extract_caption(page):
    text = page.get_text()
    lines = text.split('\n')
    for line in lines:
        match = re.search(r'(?:Figure|Fig\.)\s+(\d+)[.:\s-]+(.{20,300})', line, re.IGNORECASE)
        if match:
            return re.sub(r'\s+', ' ', match.group(2).strip())
    return ""

def extract_figures(pdf_path, paper_id):
    figures = []
    doc = fitz.open(str(pdf_path))
    seen_captions = set()
    for page_num, page in enumerate(doc):
        caption = extract_caption(page)
        if not caption or caption in seen_captions: continue
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        filename = f"{paper_id}_fig{len(figures) + 1}.png"
        filepath = ASSETS_DIR / "figures" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        pix.save(str(filepath))
        seen_captions.add(caption)
        figures.append({'filename': filename, 'caption': caption, 'page': page_num + 1, 'index': len(figures) + 1})
    doc.close()
    return figures

print("Extracting figures...")
figures = extract_figures(pdf_path, paper_id)

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
        except Exception: pass

stub = {
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
    'tags': [],
    'pdf_text': "\n".join([page.get_text() for page in fitz.open(str(pdf_path))]),
    'figures': figures,
    'references': references,
    'lead_paragraph': '', 'sections': [], 'concept_breakdown': [], 'math_equations': [], 'figure_explanations': [], 'see_also': [], 'glossary_terms': [], 'infobox_data': {}, 'main_concept': '', 'animation_path': None, 'summary': [], 'key_points': [],
}

output_path = Path(f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json")
with open(output_path, 'w') as f:
    json.dump(stub, f, indent=2)
print(f"Written to {output_path}")
