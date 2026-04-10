---
name: tidy
description: Proofread and fix a paper's content using LLM. Use /tidy <paper_id> to fix HTML artifacts, broken Figure tags, garbled sentences, and LaTeX in plain text.
version: 1.0.0
---

# Tidy Skill: Content Proofreading and Repair

The `/tidy` skill is designed to fix common quality issues in ingested papers by re-processing the stored content through an LLM.

## What it fixes:

- **Nested glossary spans:** Removes existing `<span class='glossary-term'>` tags before re-processing to avoid triple-wrapping and broken HTML.
- **Broken [[Figure X]] tags:** Ensures figure references are correct and removes them if the corresponding figure is missing.
- **Garbled sentences:** Fixes run-on sentences, mid-sentence truncations, or repetitive phrases produced by earlier LLM passes.
- **LaTeX in plain text:** Wraps math expressions in `$$...$$` blocks and fixes raw LaTeX strings that leaked into the prose.
- **Style & Tone:** Ensures a consistent, formal, yet educational Wikipedia-style tone.

## Workflow:

1.  **Read:** Fetches the paper's current data from the SQLite database (`wiki/data/wiki.db`).
2.  **Clean:** Strips out existing HTML artifacts and raw tags that might interfere with re-processing.
3.  **Proofread:** Sends the text fields (lead_paragraph, sections, concept_breakdown, glossary_terms, math_equations) to the LLM with specific instructions to fix the above issues.
4.  **Save:** Re-inserts the fixed paper data into the database.
5.  **Rebuild:** Automatically calls `generate_site()` to update the static HTML files.

## Usage:

```bash
/tidy <paper_id>
```

Example: `/tidy 2c03df8b48bf3fa39054345bafabfeff15bfd11d`

## Implementation Detail:

The skill invokes `scripts/tidy_paper.py <paper_id>`, which handles the DB operations and LLM communication.
