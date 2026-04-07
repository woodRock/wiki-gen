"""
Enhanced processor that extracts PDFs into SQLite and generates Wikipedia-style HTML.
"""

import os
import shutil
import pdf2doi
import fitz
import re
from pathlib import Path
from semanticscholar import SemanticScholar
from dotenv import load_dotenv
import json

from db_setup import (
    get_connection, init_db, insert_paper, insert_figure, 
    insert_reference, insert_glossary_term, get_paper, get_all_papers
)
from site_generator import generate_site

load_dotenv()

pdf2doi.config.set('verbose', False)

S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
sch = SemanticScholar(api_key=S2_API_KEY)

INGEST_DIR = Path("ingest")
PROCESSED_DIR = Path("processed")
ASSETS_DIR = Path("wiki/site/assets")

def ensure_dirs():
    INGEST_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def extract_figures_from_pdf(pdf_path, paper_id):
    """Extract images/figures from PDF with captions."""
    figures = []
    doc = fitz.open(str(pdf_path))
    seen_captions = set()
    
    for page_num, page in enumerate(doc):
        image_list = page.get_images(full=True)
        
        for img_idx, img in enumerate(image_list):
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

def extract_caption(page):
    """Extract caption text near a figure."""
    text = page.get_text()
    lines = text.split('\n')
    
    for line in lines:
        match = re.search(r'(?:Figure|Fig\.)\s+(\d+)[.:\s-]+(.{20,300})', line, re.IGNORECASE)
        if match:
            caption_text = match.group(2).strip()
            caption_text = re.sub(r'\s+', ' ', caption_text)
            return caption_text
    
    return ""

def extract_title_from_pdf(pdf_path):
    """Extract title from PDF's first page text."""
    doc = fitz.open(str(pdf_path))
    first_page = doc[0]
    text = first_page.get_text()
    doc.close()
    
    # Title is usually the first non-empty line
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 10:  # Skip short lines (authors, etc.)
            return line
    return None

def process_pdf(pdf_path):
    """Process a single PDF: extract metadata, figures, store in DB."""
    print(f"📄 Processing {pdf_path.name}...")
    try:
        # Get data from Semantic Scholar - try multiple strategies
        paper = None
        
        # Strategy 1: Try DOI from pdf2doi
        try:
            results = pdf2doi.pdf2doi(str(pdf_path))
            identifier = results.get('identifier')
            if identifier and '/' in identifier:
                print(f"  🔍 Trying DOI: {identifier}")
                paper = sch.get_paper(identifier)
        except Exception as e:
            print(f"  ⚠ DOI failed: {str(e)[:50]}")
            pass
        
        # Strategy 2: Extract title from PDF and search
        if not paper:
            pdf_title = extract_title_from_pdf(pdf_path)
            if pdf_title:
                print(f"  🔍 Searching by PDF title: {pdf_title[:60]}...")
                try:
                    search_results = sch.search_paper(pdf_title, limit=3)
                    if search_results:
                        # Take the first result with highest match
                        paper = search_results[0]
                        print(f"  ✓ Found: {paper.title[:60]}...")
                except Exception as e:
                    print(f"  ⚠ Title search failed: {str(e)[:50]}")
        
        # Strategy 3: Try filename-based search
        if not paper:
            title_from_filename = pdf_path.stem
            print(f"  🔍 Searching by filename: {title_from_filename}")
            try:
                search_results = sch.search_paper(title_from_filename, limit=3)
                if search_results:
                    paper = search_results[0]
            except:
                pass
        
        if not paper:
            print(f"  ❌ Could not find paper on Semantic Scholar")
            return False

        # Extract paper ID
        paper_id = paper.paperId
        
        # Extract figures
        print(f"  📊 Extracting figures...")
        figures = extract_figures_from_pdf(pdf_path, paper_id)
        print(f"  ✓ Found {len(figures)} figures")

        # Generate LLM content (summary, math, animation)
        print(f"  🤖 Generating LLM content...")
        try:
            from llm_content_gen import generate_llm_content
            llm_content = generate_llm_content(pdf_path, paper_id)
        except Exception as e:
            print(f"  ⚠ LLM content generation failed: {e}")
            llm_content = {
                'summary': [],
                'key_points': [],
                'math_equations': [],
                'glossary_terms': [],
                'animation_path': None,
                'main_concept': None
            }

        # Prepare paper data
        authors = [a.name for a in paper.authors] if paper.authors else []

        paper_data = {
            'paper_id': paper_id,
            'title': paper.title,
            'authors': authors,
            'year': paper.year,
            'venue': paper.venue or 'N/A',
            'doi': paper.externalIds.get('DOI', ''),
            'abstract': paper.abstract or 'No abstract available.',
            'tldr': paper.tldr['text'] if paper.tldr else 'N/A',
            'citation_count': paper.citationCount,
            'influential_citation_count': paper.influentialCitationCount,
            'pdf_filename': pdf_path.name,
            'tags': extract_tags(paper),
            # LLM-generated content
            'summary': llm_content.get('summary', []),
            'key_points': llm_content.get('key_points', []),
            'math_equations': llm_content.get('math_equations', []),
            'glossary_terms': llm_content.get('glossary_terms', []),
            'animation_path': llm_content.get('animation_path'),
            'main_concept': llm_content.get('main_concept')
        }

        # Store in database
        conn = get_connection()

        # Insert paper
        print(f"  💾 Storing in database...")
        insert_paper(conn, paper_data)
        
        # Insert figures
        for fig in figures:
            insert_figure(conn, paper_id, fig)
        
        # Process references
        if paper.references:
            print(f"  🔗 Processing {len(paper.references)} references...")
            for ref in paper.references[:20]:  # Top 20 refs
                try:
                    ref_data = {
                        'cited_paper_id': ref.paperId,
                        'title': ref.title,
                        'authors': [a.name for a in ref.authors] if ref.authors else [],
                        'year': ref.year,
                        'venue': ref.venue,
                        'abstract': ref.abstract,
                        'citation_count': ref.citationCount if hasattr(ref, 'citationCount') else 0,
                        'is_in_db': False  # Will be updated later
                    }
                    
                    # Check if referenced paper is in our DB
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM papers WHERE paper_id = ?", (ref.paperId,))
                    if cursor.fetchone()[0] > 0:
                        ref_data['is_in_db'] = True
                    
                    insert_reference(conn, paper_id, ref_data)
                except Exception as e:
                    print(f"    ⚠ Error processing reference: {e}")
        
        # Extract key terms for glossary
        extract_glossary_terms(conn, paper_id, paper.abstract or '')
        
        conn.commit()
        conn.close()
        
        # Move PDF to processed
        shutil.move(str(pdf_path), str(PROCESSED_DIR / pdf_path.name))
        print(f"  ✅ Done!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {pdf_path.name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def extract_tags(paper):
    """Extract topic tags from paper metadata."""
    tags = []
    
    # Extract from title and abstract
    text = f"{paper.title} {(paper.abstract or '')}".lower()
    
    # Common ML/AI topics
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
    
    return list(set(tags))[:5]  # Max 5 tags

def extract_glossary_terms(conn, paper_id, abstract):
    """Extract key terms from abstract for glossary."""
    # Common technical terms to extract
    glossary_patterns = [
        (r'(?i)(?:called|known as|termed)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'definition'),
        (r'(?i)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|are|refers to)\s+', 'definition'),
    ]
    
    # Manually defined terms based on common ML concepts
    manual_terms = {
        'Self-Attention': 'A mechanism relating different positions of a sequence to compute its representation',
        'Multi-Head Attention': 'Running several attention layers in parallel to attend to different representation subspaces',
        'Transformer': 'A sequence model based entirely on attention mechanisms, avoiding recurrence',
        'Quantization': 'Reducing precision of numerical values to save memory and computation',
        'KV Cache': 'Storage of Key-Value embeddings in language models for efficient inference',
        'JEPA': 'Joint Embedding Predictive Architecture for self-supervised learning',
        'World Model': 'A predictive model of environment dynamics for planning',
        'Embedding': 'A dense vector representation of discrete items like words or images',
    }
    
    for term, definition in manual_terms.items():
        if term.lower() in abstract.lower():
            insert_glossary_term(conn, term, definition, paper_id)

def main():
    """Main processing pipeline."""
    ensure_dirs()
    
    # Initialize database
    init_db()
    
    # Process PDFs
    pdfs = list(INGEST_DIR.glob("*.pdf"))
    if not pdfs:
        print("ℹ️  No new PDFs found in ingest/")
    else:
        print(f"📚 Found {len(pdfs)} PDF(s) to process\n")
        
        for pdf in pdfs:
            process_pdf(pdf)
            print()
    
    # Always regenerate static site
    print("\n🌐 Generating Wikipedia-style static site...")
    generate_site()
    print("✅ Site generation complete!")

if __name__ == "__main__":
    main()
