---
name: wiki-gen
description: Use this skill when working in the wiki-gen repository — a system that turns research PDFs into a Wikipedia-style static website. Activate when the user mentions ingesting papers, building the wiki, fixing paper metadata, generating animations, or managing the research knowledge base.
version: 1.0.0
---

# Wiki-Gen: Research Paper Knowledge Base

This repository turns research PDFs into a Wikipedia-style static website. You are the language model doing the analysis — no external LLM APIs are called.

## Architecture

```
ingest/          ← Drop PDFs here to process
processed/       ← PDFs move here after ingestion
wiki/
  data/wiki.db   ← SQLite database (papers, figures, glossary, references)
  site/          ← Generated static HTML site
    index.html
    paper/<id>.html
    paper/<id>.json
    assets/
      figures/   ← Extracted PDF figures
      animations/← Manim GIF animations
scripts/
  fetch_paper.py ← Semantic Scholar lookup + figure/text extraction (no LLM)
  store_paper.py ← Persist completed paper JSON to DB + move PDF + rebuild site
  site_generator.py ← Generate HTML from DB (no LLM)
  db_setup.py    ← SQLite schema and helpers
```

## Workflow

Every paper goes through two stages:

**Stage 1 — Fetch (automated, no LLM):**
```
python3 scripts/fetch_paper.py ingest/<file>.pdf
```
Produces `/tmp/wiki-gen/<paper_id>.fetch.json` containing Semantic Scholar metadata, extracted figures, and the full PDF text for you to read.

**Stage 2 — Analyse (you do this directly):**
Read the fetch JSON, read the PDF text field, and generate the Wikipedia-style content yourself. Fill in: `lead_paragraph`, `sections`, `concept_breakdown`, `math_equations`, `figure_explanations`, `see_also`, `glossary_terms`, `infobox_data`, `main_concept`, and optionally an animation.

**Stage 3 — Store (automated, no LLM):**
```
python3 scripts/store_paper.py /tmp/wiki-gen/<paper_id>.fetch.json
```
Inserts to DB, moves PDF, rebuilds site.

## Available Commands

| Command | What it does |
|---------|-------------|
| `/ingest [filename]` | Process one or all PDFs in `ingest/` |
| `/build` | Regenerate the static site from existing DB data |
| `/reingest <filename or paper_id>` | Reprocess a paper from scratch |
| `/fix-title <paper_id> <new title>` | Correct a wrong title in DB and site |

## Content Schema

When generating paper content, produce this structure (all fields are required in the JSON you write):

```json
{
  "lead_paragraph": "2-3 sentence Wikipedia-style opening.",
  "main_concept": "Short name for the paper's primary contribution",
  "infobox_data": {
    "architecture_type": "...",
    "key_innovation": "...",
    "performance_metric": "...",
    "computational_efficiency": "..."
  },
  "sections": [
    {
      "title": "Specific paper-derived section title",
      "content": "3-5 paragraphs of technical prose separated by \\n\\n",
      "figure_index": null
    }
  ],
  "concept_breakdown": [
    { "concept": "Sub-component name", "description": "2-3 sentence explanation" }
  ],
  "math_equations": [
    {
      "name": "Human-readable name",
      "latex": "LaTeX without surrounding $",
      "explanation": "Deep intuition for what this computes and why",
      "symbols": [
        { "symbol": "Q", "meaning": "Query matrix — ..." }
      ]
    }
  ],
  "figure_explanations": [
    { "figure_index": 1, "explanation": "Technical breakdown of figure content" }
  ],
  "see_also": [
    { "topic": "Related concept", "description": "One sentence connection" }
  ],
  "glossary_terms": [
    { "term": "Technical term", "definition": "Clear definition" }
  ]
}
```

**Guidelines:**
- Section titles must be paper-specific, not generic ("Scaled Dot-Product Attention" not "Method")
- Write 4–6 sections, 4–6 concept_breakdown items, 3–5 equations, 5–8 glossary terms
- Use `[[Figure X]]` in section content to reference figures; site generator converts these to bold text
- Assign `figure_index` in sections where a figure directly illustrates that section

## Manim Animations

Generate a GIF animation for each paper using Manim Community Edition:

1. Write a `.py` file to `/tmp/wiki-gen/<paper_id>_anim.py`
2. The file must: `from manim import *`, define exactly one class extending `Scene`
3. Run: `manim -v WARNING --format=gif -o <paper_id> /tmp/wiki-gen/<paper_id>_anim.py <ClassName>`
4. On error: read stderr, fix the code, retry once
5. Find the GIF: `find media -name "<paper_id>.gif" | head -1`
6. Move it: `mv <gif_path> wiki/site/assets/animations/<paper_id>.gif`
7. Set `animation_path` in the JSON: `"animations/<paper_id>.gif"`

Manim rules:
- 2D only (no ThreeDScene)
- Use `MathTex(r"...")` for math, `Text()` for labels
- `self.wait()` between steps, total runtime 10–20 seconds
- No external images or files

## Notes on Semantic Scholar Titles

Semantic Scholar sometimes returns titles with non-standard capitalisation. After ingestion, verify the title is correct and use `/fix-title` if needed. The canonical title should match the paper's own title page.
