---
name: build
description: Regenerate the wiki static site from the existing database. Use /build after making direct database edits, fixing metadata, or when site files are out of sync.
allowed-tools: [Bash]
---

# /build — Regenerate Static Site

Rebuild the entire static site from the current database state. No re-analysis, no LLM calls — pure HTML generation.

## Steps

```bash
cd /Users/woodj/Desktop/wiki-gen && python3 scripts/site_generator.py
```

If `site_generator.py` is not directly runnable (it lacks a `__main__` block), call it via:

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from site_generator import generate_site
generate_site()
"
```

## What gets regenerated

- `wiki/site/index.html` — paper grid landing page
- `wiki/site/paper/<id>.html` — individual paper pages
- `wiki/site/paper/<id>.json` — hover card data
- `wiki/site/search_index.json` — full-text search index
- `wiki/site/assets/css/wiki.css` — stylesheet
- `wiki/site/assets/js/wiki.js` — interactive features

## When to use

- After `/fix-title` or any direct DB edit
- After manually editing `site_generator.py`
- When site files are missing or corrupted
- After restoring the database from backup
