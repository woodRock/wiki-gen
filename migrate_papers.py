"""
Quick migration script to import existing processed PDFs into the new SQLite wiki.
"""

import sys
sys.path.insert(0, 'scripts')

from pathlib import Path
from db_setup import get_connection, init_db, insert_paper, insert_figure, insert_reference, insert_glossary_term
import pdf2doi
from semanticscholar import SemanticScholar
from dotenv import load_dotenv
import os
import json

load_dotenv()

pdf2doi.config.set('verbose', False)
sch = SemanticScholar(api_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY"))

PROCESSED_DIR = Path("processed")

import os

def migrate_papers():
    """Migrate all processed PDFs into the SQLite database."""
    print("🔄 Migrating existing papers to SQLite database...\n")
    
    init_db()
    conn = get_connection()
    
    pdfs = list(PROCESSED_DIR.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs to migrate\n")
    
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] Processing {pdf_path.name}...")
        
        try:
            # Get DOI/title from PDF
            results = pdf2doi.pdf2doi(str(pdf_path))
            identifier = results.get('identifier') or results.get('title')
            
            if not identifier:
                print(f"  ⚠ Could not identify, skipping")
                continue
            
            # Fetch from Semantic Scholar
            if '/' in identifier:
                paper = sch.get_paper(identifier)
            else:
                search_results = sch.search_paper(identifier, limit=1)
                if not search_results:
                    print(f"  ⚠ Not found on Semantic Scholar")
                    continue
                paper = search_results[0]
            
            paper_id = paper.paperId
            
            # Check if already in DB
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM papers WHERE paper_id = ?", (paper_id,))
            if cursor.fetchone()[0] > 0:
                print(f"  ✓ Already in database")
                continue
            
            # Prepare paper data
            paper_data = {
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
                'tags': extract_tags(paper)
            }
            
            # Insert into DB
            insert_paper(conn, paper_data)
            print(f"  ✓ Added: {paper.title[:60]}...")
            
            # Extract figures
            try:
                import fitz
                import re
                from site_generator import ensure_dirs
                ensure_dirs()
                
                figures = extract_figures_from_pdf(pdf_path, paper_id)
                for fig in figures:
                    insert_figure(conn, paper_id, fig)
                if figures:
                    print(f"  📊 Extracted {len(figures)} figures")
            except Exception as e:
                print(f"  ⚠ Figure extraction failed: {e}")
            
            # Process references
            if paper.references:
                for ref in paper.references[:20]:
                    try:
                        ref_data = {
                            'cited_paper_id': ref.paperId,
                            'title': ref.title,
                            'authors': [a.name for a in ref.authors] if ref.authors else [],
                            'year': ref.year,
                            'venue': ref.venue,
                            'abstract': ref.abstract,
                            'citation_count': ref.citationCount if hasattr(ref, 'citationCount') else 0,
                            'is_in_db': False
                        }
                        
                        cursor.execute("SELECT COUNT(*) FROM papers WHERE paper_id = ?", (ref.paperId,))
                        if cursor.fetchone()[0] > 0:
                            ref_data['is_in_db'] = True
                        
                        insert_reference(conn, paper_id, ref_data)
                    except:
                        pass
            
            conn.commit()
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    conn.close()
    print(f"\n✅ Migration complete!")
    print("🌐 Run 'python3 scripts/processor.py' to regenerate the site")

def extract_tags(paper):
    """Extract topic tags from paper."""
    tags = []
    text = f"{paper.title} {(paper.abstract or '')}".lower()
    
    topic_keywords = {
        'transformer': 'transformer',
        'attention': 'attention-mechanism',
        'quantization': 'quantization',
        'kv-cache': 'kv-cache',
        'kv cache': 'kv-cache',
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

def extract_figures_from_pdf(pdf_path, paper_id):
    """Extract figures from PDF."""
    from pathlib import Path
    figures = []
    doc = fitz.open(str(pdf_path))
    seen_captions = set()
    
    ASSETS_DIR = Path("wiki/site/assets/figures")
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    for page_num, page in enumerate(doc):
        image_list = page.get_images(full=True)
        
        for img_idx, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            
            if not base_image or len(base_image["image"]) < 10000:
                continue
            
            caption = extract_caption(page)
            if caption and caption in seen_captions:
                continue
            if caption:
                seen_captions.add(caption)
            
            filename = f"{paper_id}_fig{len(figures) + 1}.{base_image['ext']}"
            filepath = ASSETS_DIR / filename
            
            with open(filepath, "wb") as f:
                f.write(base_image["image"])
            
            figures.append({
                'filename': filename,
                'caption': caption,
                'page': page_num + 1,
                'index': len(figures) + 1
            })
    
    doc.close()
    return figures

def extract_caption(page):
    """Extract caption from page."""
    import re
    text = page.get_text()
    for line in text.split('\n'):
        match = re.search(r'(?:Figure|Fig\.)\s+(\d+)[.:\s-]+(.{20,300})', line, re.IGNORECASE)
        if match:
            return re.sub(r'\s+', ' ', match.group(2).strip())
    return ""

if __name__ == "__main__":
    migrate_papers()
