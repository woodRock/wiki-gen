"""
Store a completed paper JSON into the database and move the PDF to processed/.

Claude fills in the LLM fields (lead_paragraph, sections, math_equations, etc.)
then calls this script to persist everything and rebuild the site.

Usage:
    python3 scripts/store_paper.py /tmp/wiki-gen/<paper_id>.fetch.json
    python3 scripts/store_paper.py /tmp/wiki-gen/<paper_id>.fetch.json --no-rebuild
"""

import json
import shutil
import sys
from pathlib import Path

from db_setup import (
    get_connection, init_db, insert_paper, insert_figure,
    insert_reference, insert_glossary_term
)
from site_generator import generate_site

INGEST_DIR = Path("ingest")
PROCESSED_DIR = Path("processed")


def store_paper(json_path, rebuild_site=True):
    json_path = Path(json_path)
    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        return False

    with open(json_path) as f:
        paper_data = json.load(f)

    paper_id = paper_data['paper_id']
    print(f"Storing {paper_id} — {paper_data['title']}")

    init_db()
    conn = get_connection()

    # Insert paper record
    insert_paper(conn, paper_data)
    print(f"  Paper record inserted")

    # Insert figures
    for fig in paper_data.get('figures', []):
        insert_figure(conn, paper_id, fig)
    print(f"  {len(paper_data.get('figures', []))} figures inserted")

    # Insert references and cross-references
    for ref in paper_data.get('references', []):
        try:
            # Check if referenced paper is already in DB
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM papers WHERE paper_id = ?", (ref.get('cited_paper_id', ''),))
            ref['is_in_db'] = cursor.fetchone()[0] > 0
            insert_reference(conn, paper_id, ref)
        except Exception as e:
            print(f"  Warning: reference error: {e}")
    print(f"  {len(paper_data.get('references', []))} references inserted")

    # Insert glossary terms
    for gt in paper_data.get('glossary_terms', []):
        try:
            insert_glossary_term(conn, gt['term'], gt['definition'], paper_id)
        except Exception:
            pass

    conn.commit()
    conn.close()
    print(f"  Database committed")

    # Move PDF from ingest/ to processed/
    PROCESSED_DIR.mkdir(exist_ok=True)
    pdf_filename = paper_data.get('pdf_filename', '')
    pdf_src = INGEST_DIR / pdf_filename
    if pdf_src.exists():
        shutil.move(str(pdf_src), str(PROCESSED_DIR / pdf_filename))
        print(f"  PDF moved to processed/")
    else:
        print(f"  Note: {pdf_src} not found in ingest/ (may already be moved)")

    if rebuild_site:
        print("  Rebuilding site...")
        generate_site()

    print(f"Done: {paper_id}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/store_paper.py <json_path> [--no-rebuild]")
        sys.exit(1)

    json_path = sys.argv[1]
    rebuild = '--no-rebuild' not in sys.argv

    success = store_paper(json_path, rebuild_site=rebuild)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
