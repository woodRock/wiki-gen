---
name: fix-title
description: Fix a paper's title in the database and regenerate the site. Use /fix-title when Semantic Scholar returned the wrong capitalisation or title for a paper.
argument-hint: <paper_id> <correct title>
allowed-tools: [Read, Write, Bash]
---

# /fix-title — Correct a Paper's Title

Update a paper's title everywhere: database, JSON hover card, HTML page, and search index.

**Arguments:** `<paper_id> <correct title>`

Example: `/fix-title 204e3073870fae3d05bcbc2f6a8e263d9b72e776 Attention Is All You Need`

## Steps

### 1. Parse arguments

```
paper_id = first word of $ARGUMENTS
new_title = rest of $ARGUMENTS after the paper_id
```

### 2. Update the database

```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('wiki/data/wiki.db')
conn.execute('UPDATE papers SET title = ? WHERE paper_id = ?', ('<new_title>', '<paper_id>'))
conn.commit()
rows = conn.execute('SELECT title FROM papers WHERE paper_id = ?', ('<paper_id>',)).fetchall()
print('Updated to:', rows[0][0] if rows else 'NOT FOUND')
conn.close()
"
```

### 3. Rebuild the site

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from site_generator import generate_site
generate_site()
"
```

This regenerates:
- `wiki/site/paper/<paper_id>.html` — title in `<h1>` and `<title>`
- `wiki/site/paper/<paper_id>.json` — title in hover card data
- `wiki/site/index.html` — title on the paper grid card
- `wiki/site/search_index.json` — title in search index

### 4. Verify

Confirm the title is correct in the rebuilt HTML:
```bash
grep -m1 "<h1 id" wiki/site/paper/<paper_id>.html
```
