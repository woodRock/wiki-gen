
import json
import sqlite3
import os
import re
from pathlib import Path
from llm_content_gen import ask_llm
from db_setup import get_connection, get_paper, insert_paper
from site_generator import generate_site

def tidy_paper(paper_id):
    """
    Proofread and fix issues in a stored paper using LLM.
    Fixes: nested glossary spans, [[Figure X]] tags, garbled sentences, LaTeX in plain text.
    """
    print(f"🧹 Tidying paper {paper_id}...")
    
    conn = get_connection()
    paper = get_paper(conn, paper_id)
    if not paper:
        print(f"❌ Paper {paper_id} not found in database.")
        conn.close()
        return False
    
    # Prepare text for LLM
    # We want to fix: lead_paragraph, sections, concept_breakdown, glossary_terms
    
    # We'll send the whole structure and ask the LLM to fix it.
    # To save tokens, we only send the relevant fields.
    
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

    print("  🤖 Asking LLM to tidy content...")
    try:
        response = ask_llm(prompt)
        # Extract JSON from response
        match = re.search(r'\{[\s\S]*\}', response)
        if not match:
            print("  ❌ LLM did not return valid JSON.")
            return False
            
        fixed_fields = json.loads(match.group(0))
        
        # Update paper object with fixed fields
        for field, value in fixed_fields.items():
            paper[field] = value
            
        # Re-save to database
        print("  💾 Saving fixed paper to database...")
        insert_paper(conn, paper)
        conn.commit()
        conn.close()
        
        # Always regenerate site to reflect changes
        print("  🌐 Regenerating site...")
        generate_site()
        
        print(f"✅ Paper {paper_id} tidied successfully.")
        return True
        
    except Exception as e:
        print(f"  ❌ Error during tidy: {e}")
        import traceback
        traceback.print_exc()
        if conn: conn.close()
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        tidy_paper(sys.argv[1])
    else:
        print("Usage: python3 scripts/tidy_paper.py <paper_id>")
