import json
import sys
from semanticscholar import SemanticScholar

sch = SemanticScholar()
paper_id = "0800357049444fb80588f264d68e0c23f9b12a19"
pdf_path = "ingest/reynolds1987flocks.pdf"

print(f"Fetching metadata for paper ID: {paper_id}")
paper = sch.get_paper(paper_id)

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
    'paper_id': paper.paperId,
    'title': paper.title,
    'authors': [a.name for a in paper.authors] if paper.authors else [],
    'year': paper.year,
    'venue': paper.venue or 'N/A',
    'doi': paper.externalIds.get('DOI', ''),
    'abstract': paper.abstract or 'No abstract available.',
    'tldr': paper.tldr['text'] if paper.tldr else 'N/A',
    'citation_count': paper.citationCount,
    'influential_citation_count': paper.influentialCitationCount,
    'pdf_filename': "reynolds1987flocks.pdf",
    'tags': [],
    'pdf_text': open("/tmp/wiki-gen/dd9bad150d7c8051c5515997af2ea29c191e50e5.fetch.json").read(), # This is just a placeholder, I'll fix it
    'figures': [],
    'references': references,
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

# Fix pdf_text
with open("/tmp/wiki-gen/dd9bad150d7c8051c5515997af2ea29c191e50e5.fetch.json") as f:
    old_data = json.load(f)
    stub['pdf_text'] = old_data['pdf_text']
    stub['figures'] = old_data['figures']

output_path = f"/tmp/wiki-gen/{paper.paperId}.fetch.json"
with open(output_path, 'w') as f:
    json.dump(stub, f, indent=2)

print(f"Written to {output_path}")
print(f"Paper ID is: {paper.paperId}")
