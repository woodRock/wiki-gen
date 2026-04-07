#!/usr/bin/env python3
"""Extract figures from existing PDFs and add to existing markdown files."""

import fitz
import re
from pathlib import Path

PROCESSED_DIR = Path("processed")
DOCS_DIR = Path("wiki/docs")

# Manual mapping based on paper titles/filenames
PDF_TO_MD = {
    'han2025polarquant.pdf': 'ef9485a2522f64bca0f5cf67edc28a11984790e8.md',
    'lecun2026lewm.pdf': '530dab86cb8034bc12a32d21508aaa3f2cc00aa1.md',
    'lecun2023jepa.pdf': 'ee57e4d7a125f4ca8916284a857c3760d7d378d3.md',
    'vaswani2017attention.pdf': '204e3073870fae3d05bcbc2f6a8e263d9b72e776.md',
    'zandieh2024qjl.pdf': '7318a804566baadc9f4b4ca8255f78744e749a32.md',
    'zandieh2025turboquant.pdf': '65780e86fa36e354da618499f8b4616ac87838bf.md',
}

def extract_figures_from_pdf(pdf_path, paper_id):
    """Extract images/figures from PDF with captions using PyMuPDF."""
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
            filepath = DOCS_DIR / "assets" / filename
            
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            
            figures.append({
                'filename': filename,
                'caption': caption,
                'page': page_num + 1,
                'index': len(figures) + 1
            })
            print(f"    Figure {len(figures)}: {caption[:80] if caption else 'No caption'}")
    
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

def add_figures_to_markdown(md_file, figures):
    """Add figures section to existing markdown file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "## Figures and Diagrams" in content:
        print(f"  ⚠ Figures section already exists")
        return False
    
    figures_section = "\n## Figures and Diagrams\n\n"
    figures_section += "> Key figures extracted from the original paper.\n\n"
    
    for fig in figures:
        caption = fig['caption'] if fig['caption'] else f"Figure {fig['index']} from page {fig['page']}"
        figures_section += f"![{caption}](./assets/{fig['filename']})\n\n"
        figures_section += f"*{caption}*\n\n"
        figures_section += "---\n\n"
    
    # Insert after Abstract or Overview
    for point in ["## Abstract\n", "## Overview\n"]:
        if point in content:
            idx = content.index(point)
            next_section = content.find("\n## ", idx + len(point))
            if next_section > 0:
                content = content[:next_section] + "\n" + figures_section + "\n" + content[next_section:]
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Added {len(figures)} figures")
                return True
    
    # Fallback: insert before References
    if "## References" in content:
        idx = content.index("## References")
        content = content[:idx] + "\n" + figures_section + "\n" + content[idx:]
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Added {len(figures)} figures")
        return True
    
    return False

# Process each PDF
for pdf_name, md_name in PDF_TO_MD.items():
    pdf_path = PROCESSED_DIR / pdf_name
    md_path = DOCS_DIR / md_name
    
    if not pdf_path.exists():
        print(f"\n✗ PDF not found: {pdf_name}")
        continue
    
    if not md_path.exists():
        print(f"\n✗ Markdown not found: {md_name}")
        continue
    
    print(f"\n📄 {pdf_name} → {md_name}")
    
    paper_id = md_path.stem
    figures = extract_figures_from_pdf(pdf_path, paper_id)
    print(f"  Extracted {len(figures)} figures")
    
    if figures:
        add_figures_to_markdown(md_path, figures)

print("\n✅ Done!")
