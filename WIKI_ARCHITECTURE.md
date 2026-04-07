# Research Wiki Knowledge Base - Architecture

## Overview
A Wikipedia-style interactive knowledge base for research papers with rich cross-referencing, hover cards, and semantic connections.

## Architecture

```
PDFs → processor.py → SQLite DB → HTML Generator → Static Site
                                    ↓
                          - Wikipedia styling
                          - Hover cards (JS)
                          - Search & navigation
                          - Interactive features
```

## Database Schema (SQLite)

### papers
- paper_id (TEXT PRIMARY KEY) - Semantic Scholar ID
- title (TEXT)
- authors (TEXT) - JSON array of author names
- year (INTEGER)
- venue (TEXT)
- doi (TEXT)
- abstract (TEXT)
- tldr (TEXT)
- citation_count (INTEGER)
- influential_citation_count (INTEGER)
- pdf_filename (TEXT)
- created_at (TIMESTAMP)
- summary (TEXT) - Rich HTML summary
- tags (TEXT) - JSON array of topic tags

### figures
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- paper_id (TEXT FOREIGN KEY)
- filename (TEXT)
- caption (TEXT)
- page_num (INTEGER)
- figure_index (INTEGER)

### glossary
- term (TEXT PRIMARY KEY)
- definition (TEXT)
- paper_id (TEXT FOREIGN KEY) - where first defined
- occurrences (TEXT) - JSON of paper_ids where used

### references
- citing_paper_id (TEXT FOREIGN KEY)
- cited_paper_id (TEXT) - can be in DB or external
- title (TEXT)
- authors (TEXT)
- year (INTEGER)
- venue (TEXT)
- abstract (TEXT)
- citation_count (INTEGER)
- is_in_db (BOOLEAN) - whether cited paper has its own page

### cross_references
- from_paper_id (TEXT FOREIGN KEY)
- to_paper_id (TEXT FOREIGN KEY)
- relationship_type (TEXT) - 'cites', 'related', 'follows'
- context (TEXT) - sentence/context where mentioned

### tags
- tag (TEXT PRIMARY KEY)
- description (TEXT)
- color (TEXT) - hex color for display

### paper_tags (junction table)
- paper_id (TEXT FOREIGN KEY)
- tag (TEXT FOREIGN KEY)

## HTML Generation

### Templates
1. **index.html** - Main landing page with:
   - Paper grid/list
   - Search bar
   - Tag filters
   - Network graph visualization
   
2. **paper.html** - Individual paper pages with:
   - Wikipedia-style layout
   - Table of contents sidebar
   - Paper metadata header
   - Figures with captions
   - Animations
   - Glossary section
   - References with hover cards
   - Cited by section
   - Related papers

3. **components/**
   - hover_cards.js - Fetch and display hover cards
   - search.js - Search functionality
   - navigation.js - TOC and breadcrumbs
   - network_graph.js - Paper citation network

### Styling
- Wikipedia-inspired clean typography
- Responsive design
- Dark mode support
- Smooth animations
- Card-based layouts

## Features

### 1. Hover Cards
- **Glossary terms**: Definition appears on hover
- **References**: Title, authors, year, citations, abstract snippet
- **Internal links**: Paper preview on hover

### 2. Cross-Referencing
- Glossary terms auto-linked across all papers
- Papers that cite each other linked
- "See also" section with related papers
- Shared concepts highlighted

### 3. Search & Discovery
- Full-text search across all papers
- Filter by tags, year, authors
- "Papers citing this" and "Cited by" sections
- Citation network visualization

### 4. Rich Content
- Embedded figures with captions
- Manim animations
- Mathematical equations (MathJax)
- Code snippets with syntax highlighting

## Processing Pipeline

1. Extract DOI/title from PDF
2. Fetch metadata from Semantic Scholar
3. Extract figures with captions
4. Extract key terms for glossary
5. Generate rich HTML summary
6. Store everything in SQLite
7. Generate static HTML site
8. Build search index

## File Structure

wiki/
├── data/
│   └── wiki.db (SQLite database)
├── site/
│   ├── index.html
│   ├── paper/
│   │   └── {paper_id}.html
│   ├── assets/
│   │   ├── figures/
│   │   ├── animations/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── search_index.json
├── templates/
│   ├── base.html
│   ├── paper.html
│   └── index.html
├── scripts/
│   ├── db_setup.py
│   ├── processor.py
│   ├── site_generator.py
│   └── extract_figures.py
└── ingest/ (PDFs go here)
