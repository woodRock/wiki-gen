
import sqlite3
import json
import re
from pathlib import Path
from db_setup import get_connection, get_all_papers, get_paper, insert_paper
from llm_content_gen import ask_llm
from site_generator import generate_site

def tidy_paper_logic(conn, paper_id):
    """Internal logic to tidy a paper WITHOUT rebuilding the site."""
    paper = get_paper(conn, paper_id)
    if not paper:
        print(f"  ❌ Paper {paper_id} not found.")
        return False
    
    print(f"  🧹 Tidying: {paper['title']} ({paper_id})...")
    
    fields_to_fix = {
        'title': paper.get('title'),
        'lead_paragraph': paper.get('lead_paragraph'),
        'sections': paper.get('sections'),
        'concept_breakdown': paper.get('concept_breakdown'),
        'glossary_terms': paper.get('glossary_terms'),
        'math_equations': paper.get('math_equations'),
        'main_concept': paper.get('main_concept')
    }
    
    prompt = f"""You are a senior technical editor for a research wiki. Your task is to proofread and "tidy" the following paper data.

FIX THESE ISSUES:
1. Nested glossary spans or raw HTML artifacts: Remove any existing <span class='glossary-term'> or similar HTML tags. The system will re-add them later.
2. Broken Figure tags: Ensure [[Figure X]] is used correctly to reference figures. If a [[Figure X]] exists but there is no corresponding figure in the data, remove the tag or rephrase.
3. Garbled sentences: Fix any run-on sentences, mid-sentence truncations, or repetitive phrases.
4. LaTeX in plain text: Ensure all math expressions are wrapped in $$...$$ blocks. Fix raw LaTeX strings that leaked into plain text.
5. Tone: Ensure a formal, authoritative, yet educational Wikipedia-style tone.

PAPER DATA (JSON):
{json.dumps(fields_to_fix, indent=2)}

RETURN:
Return the EXACT same JSON structure, but with all text fields proofread and fixed according to the rules above. Return ONLY valid JSON. No markdown, no commentary.
"""

    try:
        response = ask_llm(prompt)
        match = re.search(r'\{[\s\S]*\}', response)
        if not match:
            print("    ❌ LLM did not return valid JSON.")
            return False
            
        fixed_fields = json.loads(match.group(0))
        for field, value in fixed_fields.items():
            paper[field] = value
            
        insert_paper(conn, paper)
        conn.commit()
        print("    ✅ Done.")
        return True
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False

def tidy_all():
    conn = get_connection()
    papers = get_all_papers(conn)
    print(f"Starting batch tidy for {len(papers)} papers...")
    
    for p in papers:
        tidy_paper_logic(conn, p['paper_id'])
    
    conn.close()
    print("✨ Batch tidy complete. Regenerating site...")
    generate_site()
    print("🚀 All papers tidied and site rebuilt!")

if __name__ == "__main__":
    tidy_all()
