---
name: ingest
description: Process research PDFs from the ingest/ directory into the wiki. Drop PDF files in ingest/ then run /ingest to turn them into Wikipedia-style pages.
argument-hint: [filename.pdf]
allowed-tools: [Read, Write, Bash, Glob]
---

# /ingest — Process Research Papers

Ingest one or all PDFs from `ingest/` into the wiki database and regenerate the site.

**Argument:** optional PDF filename. If omitted, process all PDFs in `ingest/`.

## Steps

### 1. Identify PDFs to process

If `$ARGUMENTS` is provided, process that specific file: `ingest/$ARGUMENTS`
Otherwise list all PDFs:
```bash
ls ingest/*.pdf
```

### 2. For each PDF — fetch metadata (non-LLM)

```bash
python3 scripts/fetch_paper.py ingest/<filename>.pdf
```

This produces `/tmp/wiki-gen/<paper_id>.fetch.json` with:
- Semantic Scholar metadata (title, authors, year, venue, abstract, references)
- Extracted figures saved to `wiki/site/assets/figures/`
- Full PDF text in the `pdf_text` field

Read the output JSON to get the paper_id and all metadata.

### 3. For each PDF — analyse the paper (you do this)

Read the `pdf_text` from the JSON. Then generate Wikipedia-style content directly:

**lead_paragraph** — 2-3 sentence opening stating what the paper introduces, what problem it solves, and its significance. Be specific; cite numbers or results if striking.

**main_concept** — Short name for the paper's primary contribution (e.g. "Scaled Dot-Product Attention").

**infobox_data** — Four fields: `architecture_type`, `key_innovation`, `performance_metric`, `computational_efficiency`.

**sections** — 4-6 sections with paper-specific titles (not "Method" — use the actual mechanism name). Each section needs 3-5 paragraphs of technical prose. Assign `figure_index` where a figure illustrates the section.

**concept_breakdown** — 4-6 sub-components, each with a 2-3 sentence technical description.

**math_equations** — 3-5 key equations with full LaTeX, deep intuition, and symbol-by-symbol breakdowns.

**figure_explanations** — Explain every extracted figure technically: axes, data flow, architecture depicted.

**see_also** — 4-6 related concepts or papers with one-sentence connections.

**glossary_terms** — 5-8 technical terms with clear definitions.

### 4. For each PDF — generate Manim animation (optional but encouraged)

Write Manim CE Python code that visualises the core concept:

```bash
# Write the animation script
# Then render it:
manim -v WARNING --format=gif -o <paper_id> /tmp/wiki-gen/<paper_id>_anim.py <SceneClassName>
# If it fails, fix and retry once.
# Find and move the GIF:
find media -name "<paper_id>.gif" | head -1
mv <gif_path> wiki/site/assets/animations/<paper_id>.gif
```

Set `animation_path` to `"animations/<paper_id>.gif"` in the JSON if successful.

### 5. Write the completed JSON

Merge your generated content into the fetch JSON and write it back to `/tmp/wiki-gen/<paper_id>.fetch.json`. All LLM fields must be populated before storing.

### 6. Store to database and rebuild site

```bash
python3 scripts/store_paper.py /tmp/wiki-gen/<paper_id>.fetch.json
```

This inserts the paper into the DB, moves the PDF to `processed/`, and regenerates the static site.

### 7. Verify

After each paper, confirm:
- Paper appears in `wiki/site/index.html`
- Individual page exists at `wiki/site/paper/<paper_id>.html`
- PDF is no longer in `ingest/`

## Post-ingestion title check

After ingestion, always check whether Semantic Scholar returned the correct title. If it differs from the paper's own title page, run `/fix-title <paper_id> <correct title>`.
