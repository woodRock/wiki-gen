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
        identifier = None

        # Strategy 1: DOI/identifier from pdf2doi
        try:
            results = pdf2doi.pdf2doi(str(pdf_path))
            identifier = results.get('identifier')
        except Exception as e:
            print(f"  ⚠ pdf2doi failed: {str(e)[:50]}")

        if identifier:
            # Strategy 1a: arXiv ID (most reliable for preprints)
            arxiv_match = re.search(r'arxiv[./](\d{4}\.\d{4,5})', identifier, re.IGNORECASE)
            if arxiv_match:
                arxiv_id = arxiv_match.group(1)
                print(f"  🔍 Trying arXiv ID: {arxiv_id}")
                try:
                    paper = sch.get_paper(f"arXiv:{arxiv_id}")
                except Exception as e:
                    print(f"  ⚠ arXiv lookup failed: {str(e)[:50]}")

            # Strategy 1b: Raw DOI
            if not paper and '/' in identifier:
                print(f"  🔍 Trying DOI: {identifier}")
                try:
                    paper = sch.get_paper(identifier)
                except Exception as e:
                    print(f"  ⚠ DOI failed: {str(e)[:50]}")

        # Strategy 2: Extract title from PDF and search
        if not paper:
            pdf_title = extract_title_from_pdf(pdf_path)
            if pdf_title and len(pdf_title.split()) >= 5:
                print(f"  🔍 Searching by PDF title: {pdf_title[:60]}...")
                try:
                    search_results = sch.search_paper(pdf_title, limit=3)
                    if search_results:
                        paper = search_results[0]
                        print(f"  ✓ Found: {paper.title[:60]}...")
                except Exception as e:
                    print(f"  ⚠ Title search failed: {str(e)[:50]}")

        # Strategy 3: Filename-derived search (last resort)
        if not paper:
            stem = pdf_path.stem
            query = re.sub(r'^[a-z]+\d{4}', '', stem).replace('_', ' ').strip() or stem
            print(f"  🔍 Searching by filename query: {query}")
            try:
                search_results = sch.search_paper(query, limit=3)
                if search_results:
                    paper = search_results[0]
                    print(f"  ✓ Found: {paper.title[:60]}...")
            except Exception:
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
            llm_content = generate_llm_content(
                pdf_path, paper_id,
                paper_title=paper.title,
                figures=figures,
            )
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
            # LLM-generated content
            'summary': llm_content.get('summary', []),
            'key_points': llm_content.get('key_points', []),
            'math_equations': llm_content.get('math_equations', []),
            'glossary_terms': llm_content.get('glossary_terms', []),
            'concept_breakdown': llm_content.get('concept_breakdown', []),
            'infobox_data': llm_content.get('infobox_data', {}),
            'lead_paragraph': llm_content.get('lead_paragraph', ''),
            'sections': llm_content.get('sections', []),
            'figure_explanations': llm_content.get('figure_explanations', []),
            'see_also': llm_content.get('see_also', []),
            'animation_path': llm_content.get('animation_path'),
            'main_concept': llm_content.get('main_concept')
        }

        # Extract tags using all available data
        paper_data['tags'] = extract_tags(paper_data)

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
        
        # Insert LLM-generated glossary terms
        for gt in llm_content.get('glossary_terms', []):
            try:
                insert_glossary_term(conn, gt['term'], gt['definition'], paper_id)
            except Exception:
                pass

        # Extract key terms from abstract (fallback heuristics)
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

def extract_tags(paper_data):
    """Extract topic tags from paper metadata and LLM-generated content."""
    tags = []
    
    # Extract from title and abstract
    parts = [
        paper_data.get('title', ''),
        paper_data.get('abstract', '') or '',
        paper_data.get('lead_paragraph', '') or '',
        paper_data.get('main_concept', '') or '',
    ]
    
    # Add sections and concept breakdown if available
    sections = paper_data.get('sections', [])
    for section in sections:
        parts.append(section.get('title', ''))
        parts.append(section.get('content', ''))
        
    concepts = paper_data.get('concept_breakdown', [])
    for concept in concepts:
        parts.append(concept.get('concept', ''))
        parts.append(concept.get('description', ''))
        
    text = ' '.join(parts).lower()
    
    # Robust keyword matching - same as in site_generator.py
    TAG_KEYWORDS = {
        "transformer": ["transformer", "attention is all you need", "bert", "gpt", "t5", "encoder-decoder"],
        "attention-mechanism": ["attention mechanism", "self-attention", "multi-head attention", "cross-attention", "scaled dot-product"],
        "computer-vision": ["image", "vision", "convolutional", "cnn", "object detection", "segmentation", "resnet", "vit", "visual"],
        "large-language-models": ["large language model", "llm", "gpt", "language model", "foundation model", "instruction tuning", "rlhf", "chat"],
        "generative-models": ["generative", "gan", "diffusion", "vae", "variational autoencoder", "image synthesis", "stable diffusion", "denoising"],
        "recurrent-networks": ["recurrent", "lstm", "gru", "rnn", "sequence model", "seq2seq"],
        "optimization": ["optimization", "gradient descent", "adam", "sgd", "learning rate", "convergence", "loss function"],
        "regularization": ["regularization", "dropout", "batch normalization", "weight decay", "overfitting", "l2"],
        "embeddings": ["embedding", "word2vec", "glove", "representation learning", "vector space", "token embedding"],
        "quantization": ["quantization", "quantized", "int8", "mixed precision", "model compression", "pruning"],
        "self-supervised-learning": ["self-supervised", "contrastive", "masked language model", "pretraining", "pre-training", "SimCLR", "BYOL"],
        "world-models": ["world model", "model-based", "environment model", "dreamer", "imagination"],
        "latent-space": ["latent space", "latent representation", "latent variable", "bottleneck", "encoding"],
        "jepa": ["jepa", "joint embedding predictive", "energy-based"],
    }
    
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                tags.append(tag)
                break
    
    return list(set(tags))[:8]  # Max 8 tags

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

def reingest_all():
    """Move all processed PDFs back to ingest/ and wipe the database for a clean rerun."""
    import sqlite3
    from db_setup import DB_PATH

    processed_pdfs = list(PROCESSED_DIR.glob("*.pdf"))
    if not processed_pdfs:
        print("ℹ️  No PDFs found in processed/")
        return

    print(f"♻️  Moving {len(processed_pdfs)} PDF(s) back to ingest/...")
    for pdf in processed_pdfs:
        shutil.copy(str(pdf), str(INGEST_DIR / pdf.name))

    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"🗑️  Cleared database {DB_PATH}")

    print()


def main():
    """Main processing pipeline."""
    import sys
    if "--reingest" in sys.argv:
        reingest_all()

    # Provider support
    provider = "gemini"
    for arg in sys.argv:
        if arg.startswith("--provider="):
            provider = arg.split("=")[1]
    
    os.environ["LLM_PROVIDER"] = provider
    print(f"🚀 Using LLM Provider: {provider}")

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
