---
name: reingest
description: Reprocess a paper from scratch — re-fetch metadata, re-analyse content, regenerate animation. Use /reingest when a paper's content is wrong, outdated, or Semantic Scholar returned bad data.
argument-hint: <filename.pdf or paper_id>
allowed-tools: [Read, Write, Bash, Glob]
---

# /reingest — Reprocess a Paper

Wipe a paper's DB record and reprocess it end-to-end.

**Argument:** PDF filename (e.g. `vaswani2017attention.pdf`) or Semantic Scholar paper ID.

## Steps

### 1. Identify the paper

If given a PDF filename, find the paper_id by checking:
```bash
python3 -c "
import sys, json, sqlite3
sys.path.insert(0, 'scripts')
conn = sqlite3.connect('wiki/data/wiki.db')
conn.row_factory = sqlite3.Row
rows = conn.execute('SELECT paper_id, title, pdf_filename FROM papers').fetchall()
for r in rows: print(r['paper_id'], r['pdf_filename'], r['title'])
"
```

If given a paper_id directly, skip this step.

### 2. Copy PDF back to ingest/

The PDF will be in `processed/`. Copy it back:
```bash
cp processed/<filename>.pdf ingest/
```

### 3. Delete the paper from the database

```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('wiki/data/wiki.db')
conn.execute('PRAGMA foreign_keys=ON')
conn.execute('DELETE FROM papers WHERE paper_id = ?', ('<paper_id>',))
conn.commit()
print('Deleted')
"
```
This cascades to figures, references, cross-references, and paper_tags.

### 4. Process the paper

Follow the full `/ingest` workflow for this single PDF:
- `python3 scripts/fetch_paper.py ingest/<filename>.pdf`
- Analyse the paper and generate content
- Generate Manim animation
- `python3 scripts/store_paper.py /tmp/wiki-gen/<paper_id>.fetch.json`

### 5. Title check

After reingestion, verify the title matches the paper's own title page. Semantic Scholar sometimes uses non-standard capitalisation. If wrong, run `/fix-title`.

## Notes

- Old figures in `wiki/site/assets/figures/` with the paper's ID prefix are overwritten by fresh extraction.
- Old animation GIFs are not automatically deleted — delete manually if regenerating: `rm wiki/site/assets/animations/<paper_id>.gif`
