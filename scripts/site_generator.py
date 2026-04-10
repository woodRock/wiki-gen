"""
Generate Wikipedia-style static HTML site from SQLite database.
"""

import json
import re
import math
from pathlib import Path
from db_setup import get_connection, get_all_papers, get_paper, get_glossary

SITE_DIR = Path("wiki/site")

# ---------------------------------------------------------------------------
# Tag inference
# ---------------------------------------------------------------------------

TAG_KEYWORDS = {
    "transformer": ["transformer", "attention is all you need", "bert", "gpt", "t5", "encoder-decoder"],
    "attention-mechanism": ["attention mechanism", "self-attention", "multi-head attention", "cross-attention", "scaled dot-product"],
    "computer-vision": ["image", "vision", "convolutional", "cnn", "object detection", "segmentation", "resnet", "vit", "visual"],
    "large-language-models": ["large language model", "llm", "gpt", "language model", "foundation model", "instruction tuning", "rlhf", "chat"],
    "generative-models": ["generative", "gan", "diffusion", "vae", "variational autoencoder", "image synthesis", "stable diffusion", "denoising"],
    "recurrent-networks": ["recurrent", "lstm", "gru", "rnn", "sequence model", "seq2seq"],
    "optimization": ["optimization", "gradient descent", "adam", "sgd", "learning rate", "convergence", "loss function"],
    "regularization": ["regularization", "dropout", "batch normalization", "weight decay", "overfitting", "l2"],
    "embeddings": ["embedding", "word2vec", "glove", "representation learning", "vector space", "token embedding"],
    "quantization": ["quantization", "quantized", "int8", "mixed precision", "model compression", "pruning"],
    "self-supervised-learning": ["self-supervised", "contrastive", "masked language model", "pretraining", "pre-training", "SimCLR", "BYOL"],
    "world-models": ["world model", "model-based", "environment model", "dreamer", "imagination"],
    "latent-space": ["latent space", "latent representation", "latent variable", "bottleneck", "encoding"],
    "jepa": ["jepa", "joint embedding predictive", "energy-based"],
}


def infer_tags(paper):
    """Infer tags for a paper based on keyword matching."""
    # Build corpus text
    parts = [
        paper.get('title', ''),
        paper.get('lead_paragraph', ''),
        paper.get('main_concept', ''),
    ]
    for section in paper.get('sections', []):
        parts.append(section.get('title', ''))
    for concept in paper.get('concept_breakdown', []):
        parts.append(concept.get('concept', ''))

    corpus = ' '.join(parts).lower()

    inferred = []
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in corpus:
                inferred.append(tag)
                break

    return inferred


def generate_site():
    """Generate complete Wikipedia-style static site."""
    conn = get_connection()

    # Create directories
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / "paper").mkdir(exist_ok=True)
    (SITE_DIR / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (SITE_DIR / "assets" / "js").mkdir(parents=True, exist_ok=True)

    # Copy assets
    copy_assets()

    # Fetch basic papers list and glossary
    papers_basic = get_all_papers(conn)
    glossary = get_glossary(conn)

    # Generate individual paper pages (full data)
    for paper_data in papers_basic:
        paper = get_paper(conn, paper_data['paper_id'])

        # Infer tags if missing
        if not paper.get('tags'):
            inferred = infer_tags(paper)
            paper['tags'] = inferred
            paper_data['tags'] = inferred

        generate_paper_page(paper, glossary)

    # Generate index page
    generate_index(papers_basic, glossary)

    # Generate search index
    generate_search_index(papers_basic, conn)

    # Generate timeline
    generate_timeline(papers_basic)

    # Generate citation graph
    generate_graph(papers_basic, conn)

    conn.close()
    print(f"✅ Generated site in {SITE_DIR}")


def copy_assets():
    """Copy CSS and JS files."""
    css_content = """
/* Wikipedia-style styling for Research Wiki */

:root {
  --wiki-bg: #ffffff;
  --wiki-text: #202122;
  --wiki-link: #3366cc;
  --wiki-link-hover: #447ff5;
  --wiki-border: #a2a9b1;
  --wiki-gray-bg: #f8f9fa;
  --wiki-info-bg: #eaf3ff;
  --wiki-success-bg: #d5fdd5;
  --wiki-warning-bg: #fef6e7;
  --primary-color: #4A90E2;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: sans-serif;
  line-height: 1.6;
  color: var(--wiki-text);
  background: var(--wiki-bg);
  padding-bottom: 50px;
}

/* Header */
.wiki-header {
  background: var(--wiki-bg);
  border-bottom: 1px solid var(--wiki-border);
  padding: 0.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}

.wiki-logo {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--wiki-text);
  text-decoration: none;
  font-family: 'Linux Libertine', 'Georgia', 'Times', serif;
}

.wiki-search {
  flex: 0 1 400px;
}

.wiki-search input {
  width: 100%;
  padding: 0.3rem 1rem;
  border: 1px solid var(--wiki-border);
  border-radius: 2px;
  font-size: 0.85rem;
}

/* Main content */
.wiki-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
  display: flex;
  gap: 2rem;
}

/* Sidebar / TOC */
.wiki-sidebar {
  width: 200px;
  flex-shrink: 0;
  font-size: 0.85rem;
}

.wiki-sidebar h3 {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #54595d;
  margin-bottom: 0.5rem;
  padding-bottom: 0.2rem;
  border-bottom: 1px solid var(--wiki-border);
}

.wiki-sidebar ul {
  list-style: none;
  margin-bottom: 1.5rem;
}

.wiki-sidebar li {
  margin-bottom: 0.2rem;
}

.wiki-sidebar a {
  color: var(--wiki-link);
  text-decoration: none;
  display: block;
  padding: 0.1rem 0;
}

.wiki-sidebar a:hover {
  text-decoration: underline;
}

/* Article */
.wiki-article {
  flex-grow: 1;
  min-width: 0;
}

.wiki-article h1 {
  font-size: 1.8rem;
  font-weight: normal;
  border-bottom: 1px solid var(--wiki-border);
  padding-bottom: 0.2rem;
  margin-bottom: 0.5rem;
  font-family: 'Linux Libertine', 'Georgia', 'Times', serif;
}

.wiki-article .lead {
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.wiki-article h2 {
  font-size: 1.5rem;
  font-weight: normal;
  border-bottom: 1px solid var(--wiki-border);
  padding-bottom: 0.2rem;
  margin: 2rem 0 0.8rem;
  font-family: 'Linux Libertine', 'Georgia', 'Times', serif;
}

.wiki-article h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 1.5rem 0 0.5rem;
  border-bottom: none;
}

.wiki-article p {
  margin-bottom: 1rem;
  text-align: justify;
}

/* Infobox */
.infobox {
  float: right;
  width: 300px;
  background: var(--wiki-gray-bg);
  border: 1px solid var(--wiki-border);
  padding: 0.2rem;
  margin-left: 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  clear: right;
}

.infobox-title {
  background: #cedff2;
  text-align: center;
  font-weight: bold;
  padding: 0.5rem;
  font-size: 1rem;
  margin-bottom: 0.2rem;
}

.infobox-image {
  text-align: center;
  padding: 0.5rem;
  background: #fff;
}

.infobox-image img {
  max-width: 100%;
  height: auto;
}

.infobox table {
  width: 100%;
  border-collapse: collapse;
}

.infobox th {
  text-align: left;
  padding: 0.3rem 0.5rem;
  vertical-align: top;
  width: 40%;
}

.infobox td {
  padding: 0.3rem 0.5rem;
}

/* Thumbnails (figures) */
.thumb {
  clear: right;
  float: right;
  margin: 0.5rem 0 1.3rem 1.4rem;
  background-color: #f8f9fa;
  border: 1px solid #c8ccd1;
  padding: 3px;
  width: 300px;
}

.thumbinner {
  padding: 3px;
  text-align: center;
  overflow: hidden;
}

.thumbimage {
  border: 1px solid #c8ccd1;
  max-width: 100%;
  height: auto;
  display: block;
}

.thumbcaption {
  border: none;
  font-size: 0.8rem;
  line-height: 1.4;
  padding: 3px;
  text-align: left;
  background-color: #f8f9fa;
}

/* Math */
.math-block {
  margin: 1.5rem 2rem;
  padding: 1rem;
  background: #fdfdfd;
  border: 1px solid #eaecf0;
  text-align: center;
  position: relative;
}

.math-explanation-box {
  margin: 1rem 0 2rem;
  padding: 1rem;
  background: var(--wiki-info-bg);
  border-left: 5px solid var(--wiki-link);
  font-size: 0.9rem;
}

.symbol-table {
  width: 100%;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  border-top: 1px solid var(--wiki-border);
}

.symbol-table th { text-align: left; padding: 2px 5px; border-bottom: 1px solid #eee; }
.symbol-table td { padding: 2px 5px; border-bottom: 1px solid #eee; }

/* Concept breakdown */
.concept-item {
  margin-bottom: 1.5rem;
  padding-left: 1rem;
  border-left: 3px solid #cedff2;
}

.concept-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.3rem;
  color: #000;
}

/* See Also */
.see-also-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.see-also-item {
  background: var(--wiki-gray-bg);
  padding: 0.8rem;
  border-radius: 4px;
  border: 1px solid var(--wiki-border);
}

.see-also-item b {
  display: block;
  color: var(--wiki-link);
  margin-bottom: 0.2rem;
}

/* Glossary terms */
.glossary-term {
  border-bottom: 1px dotted #3366cc;
  cursor: help;
  color: inherit;
}

/* Index page */
.paper-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.paper-card {
  background: var(--wiki-bg);
  border: 1px solid var(--wiki-border);
  padding: 1rem;
  transition: background 0.1s;
  cursor: pointer;
}

.paper-card:hover {
  background: #f8f9fa;
}

.paper-card h3 {
  font-size: 1.1rem;
  margin-bottom: 0.3rem;
  color: var(--wiki-link);
  font-family: 'Linux Libertine', serif;
}

/* Footer */
.wiki-footer {
  border-top: 1px solid var(--wiki-border);
  padding: 2rem;
  margin-top: 4rem;
  font-size: 0.75rem;
  color: #54595d;
  background: var(--wiki-gray-bg);
}

/* Tags */
.tag {
  display: inline-block;
  padding: 0.15rem 0.55rem;
  margin: 0.15rem 0.2rem 0.15rem 0;
  border-radius: 3px;
  font-size: 0.78rem;
  font-weight: 500;
  white-space: nowrap;
}

/* Hover card */
.hover-card {
  display: none;
  position: fixed;
  z-index: 500;
  background: #fff;
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
  padding: 0.8rem 1rem;
  max-width: 320px;
  min-width: 200px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  font-size: 0.85rem;
  line-height: 1.5;
  pointer-events: none;
}

.hover-card.visible {
  display: block;
}

.hover-card h4 {
  margin: 0 0 0.4rem;
  font-size: 0.95rem;
  font-weight: bold;
  color: var(--wiki-text);
  font-family: 'Linux Libertine', 'Georgia', 'Times', serif;
  border-bottom: 1px solid var(--wiki-border);
  padding-bottom: 0.3rem;
}

.hover-card .meta {
  color: #54595d;
  font-size: 0.78rem;
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.hover-card .abstract {
  color: var(--wiki-text);
  font-size: 0.83rem;
}

/* Search dropdown */
.wiki-search {
  position: relative;
}

.wiki-search input:focus {
  outline: none;
  border-color: var(--wiki-link);
  box-shadow: 0 0 0 2px rgba(51,102,204,0.15);
}

.search-dropdown {
  display: none;
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
  max-height: 480px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12), 0 2px 6px rgba(0,0,0,0.07);
  animation: searchFadeIn 0.1s ease-out;
}

@keyframes searchFadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}

.search-dropdown.visible {
  display: block;
}

.search-result-count {
  padding: 0.35rem 1rem;
  font-size: 0.68rem;
  color: #72777d;
  background: var(--wiki-gray-bg);
  border-bottom: 1px solid var(--wiki-border);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.search-result {
  padding: 0.6rem 1rem 0.6rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  border-left: 3px solid transparent;
  transition: background 0.08s, border-color 0.08s;
}

.search-result:hover,
.search-result.active {
  background: #f3f8ff;
  border-left-color: var(--wiki-link);
}

.search-result:last-child {
  border-bottom: none;
}

.search-result-title {
  font-weight: 500;
  color: var(--wiki-link);
  font-size: 0.88rem;
  line-height: 1.35;
  margin-bottom: 0.2rem;
}

.search-result-title mark {
  background: #fff3b0;
  color: inherit;
  border-radius: 2px;
  padding: 0 1px;
  font-style: normal;
}

.search-result-meta {
  font-size: 0.72rem;
  color: #72777d;
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

.search-result-meta .sep {
  margin: 0 0.3rem;
  opacity: 0.5;
}

.search-result-meta .year {
  font-weight: 600;
  color: #54595d;
}

.search-result-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.search-result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem;
}

.search-result-tag {
  padding: 0.1rem 0.45rem;
  background: #e8f0fe;
  color: #1a56b0;
  border-radius: 10px;
  font-size: 0.67rem;
  font-weight: 500;
}

.search-result-citations {
  font-size: 0.68rem;
  color: #999;
  white-space: nowrap;
  flex-shrink: 0;
}

.search-no-results {
  padding: 1.2rem 1rem;
  color: #72777d;
  font-size: 0.85rem;
  font-style: italic;
  text-align: center;
}

/* Dark mode overrides */
[data-theme="dark"] {
  --wiki-bg: #1a1a1a;
  --wiki-text: #e8e8e8;
  --wiki-link: #7aadff;
  --wiki-link-hover: #99c0ff;
  --wiki-border: #444;
  --wiki-gray-bg: #252525;
  --wiki-info-bg: #1e2a3a;
}

[data-theme="dark"] body {
  background: var(--wiki-bg);
  color: var(--wiki-text);
}

[data-theme="dark"] .wiki-header {
  background: #111;
  border-bottom-color: #444;
}

[data-theme="dark"] .wiki-search input {
  background: #2a2a2a;
  color: #e8e8e8;
  border-color: #555;
}

[data-theme="dark"] .search-dropdown {
  background: #2a2a2a;
  border-color: #555;
}

[data-theme="dark"] .search-result:hover,
[data-theme="dark"] .search-result.active {
  background: #333;
}

[data-theme="dark"] .paper-card {
  background: #252525;
  border-color: #444;
}

[data-theme="dark"] .paper-card:hover {
  background: #2e2e2e;
}

[data-theme="dark"] .infobox {
  background: #252525;
  border-color: #444;
}

[data-theme="dark"] .infobox-title {
  background: #2a3a50;
}

[data-theme="dark"] .hover-card {
  background: #2a2a2a;
  border-color: #555;
  color: var(--wiki-text);
}

[data-theme="dark"] .wiki-footer {
  background: #1e1e1e;
  border-color: #444;
  color: #aaa;
}

[data-theme="dark"] .see-also-item {
  background: #252525;
  border-color: #444;
}

[data-theme="dark"] .math-block {
  background: #222;
  border-color: #444;
}

[data-theme="dark"] .math-explanation-box {
  background: #1e2a3a;
}

[data-theme="dark"] .concept-item {
  border-left-color: #2a3a50;
}

[data-theme="dark"] .thumb {
  background-color: #252525;
  border-color: #444;
}

[data-theme="dark"] .thumbcaption {
  background-color: #252525;
}

[data-theme="dark"] .related-card {
  background: #252525;
  border-color: #444;
}

[data-theme="dark"] .related-card:hover {
  background: #2e2e2e;
}

[data-theme="dark"] .timeline-group {
  border-left-color: #444;
}

[data-theme="dark"] .timeline-paper {
  background: #252525;
  border-color: #444;
}

[data-theme="dark"] .timeline-paper:hover {
  background: #2e2e2e;
}

/* Nav links and dark mode toggle */
.wiki-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.85rem;
}

.wiki-nav a {
  color: var(--wiki-link);
  text-decoration: none;
}

.wiki-nav a:hover {
  text-decoration: underline;
}

.dark-toggle {
  background: none;
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
  padding: 0.25rem 0.6rem;
  font-size: 0.82rem;
  cursor: pointer;
  color: var(--wiki-text);
  white-space: nowrap;
}

.dark-toggle:hover {
  background: var(--wiki-gray-bg);
}

/* Reading progress bar */
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 0%;
  background: var(--wiki-link);
  z-index: 9999;
  transition: width 0.1s linear;
}

/* Index toolbar */
.index-toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--wiki-border);
}

.toolbar-label {
  font-size: 0.78rem;
  color: #54595d;
  font-weight: 600;
  margin-right: 0.2rem;
}

.sort-btn, .filter-tag-btn, .clear-btn, .random-btn {
  border: 1px solid var(--wiki-border);
  border-radius: 3px;
  padding: 0.2rem 0.6rem;
  font-size: 0.78rem;
  cursor: pointer;
  background: var(--wiki-bg);
  color: var(--wiki-text);
  transition: background 0.1s, border-color 0.1s;
}

.sort-btn:hover, .filter-tag-btn:hover, .clear-btn:hover, .random-btn:hover {
  background: var(--wiki-gray-bg);
}

.sort-btn.active {
  background: var(--wiki-link);
  color: #fff;
  border-color: var(--wiki-link);
}

.filter-tag-btn.active {
  background: #e8f0fe;
  color: #1a56b0;
  border-color: #7aadff;
}

.toolbar-sep {
  width: 1px;
  height: 1.2rem;
  background: var(--wiki-border);
  margin: 0 0.2rem;
}

.random-btn {
  margin-left: auto;
  background: var(--wiki-gray-bg);
}

.paper-card.hidden {
  display: none;
}

.no-results-msg {
  grid-column: 1 / -1;
  padding: 2rem;
  text-align: center;
  color: #72777d;
  font-style: italic;
}

/* Related papers grid */
.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}

.related-card {
  background: var(--wiki-gray-bg);
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
  padding: 0.8rem;
  cursor: pointer;
  transition: background 0.1s;
}

.related-card:hover {
  background: #e3eeff;
}

.related-card-title {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--wiki-link);
  margin-bottom: 0.3rem;
  line-height: 1.35;
}

.related-card-meta {
  font-size: 0.75rem;
  color: #72777d;
}

/* Timeline page */
.timeline-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
}

.timeline-group {
  position: relative;
  padding-left: 2rem;
  margin-bottom: 2.5rem;
  border-left: 2px solid var(--wiki-border);
}

.timeline-year-label {
  position: absolute;
  left: -1rem;
  top: 0;
  background: var(--wiki-link);
  color: #fff;
  font-weight: bold;
  font-size: 0.85rem;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  transform: translateX(-50%);
  white-space: nowrap;
}

.timeline-papers {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  padding-top: 1.5rem;
}

.timeline-paper {
  background: var(--wiki-bg);
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
  padding: 0.7rem 1rem;
  cursor: pointer;
  transition: background 0.1s;
}

.timeline-paper:hover {
  background: var(--wiki-gray-bg);
}

.timeline-paper-title {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--wiki-link);
  margin-bottom: 0.2rem;
}

.timeline-paper-meta {
  font-size: 0.78rem;
  color: #72777d;
}

/* Graph page */
#graph-canvas {
  display: block;
  width: 100%;
  height: calc(100vh - 120px);
  cursor: grab;
  background: var(--wiki-gray-bg);
  border: 1px solid var(--wiki-border);
}

#graph-canvas:active {
  cursor: grabbing;
}

.graph-tooltip {
  display: none;
  position: fixed;
  z-index: 500;
  background: var(--wiki-bg);
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
  padding: 0.6rem 0.8rem;
  max-width: 280px;
  font-size: 0.82rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  pointer-events: none;
  line-height: 1.4;
}

.graph-tooltip.visible {
  display: block;
}

.graph-hint {
  font-size: 0.75rem;
  color: #72777d;
  text-align: center;
  margin-top: 0.4rem;
}

/* Responsive */
@media (max-width: 900px) {
  .wiki-content {
    flex-direction: column-reverse;
  }
  .wiki-sidebar {
    width: 100%;
  }
  .infobox, .thumb {
    float: none;
    width: 100%;
    margin-left: 0;
  }
}
"""

    with open(SITE_DIR / "assets" / "css" / "wiki.css", 'w', encoding='utf-8') as f:
        f.write(css_content)

    # Main JS
    js_content = """
// Wikipedia-style interactive features

// Hover card system
class HoverCard {
  constructor() {
    this.card = null;
    this.currentTimeout = null;
    this.init();
  }

  init() {
    this.createCard();
    this.setupListeners();
  }

  createCard() {
    this.card = document.createElement('div');
    this.card.className = 'hover-card';
    document.body.appendChild(this.card);
  }

  setupListeners() {
    // Reference hover cards
    document.querySelectorAll('.reference-link[data-paper-id]').forEach(link => {
      link.addEventListener('mouseenter', (e) => {
        const paperId = e.target.dataset.paperId;
        this.showReferenceCard(e.target, paperId);
      });

      link.addEventListener('mouseleave', () => {
        this.hideCard();
      });
    });

    // Glossary term hover cards
    document.querySelectorAll('.glossary-term').forEach(term => {
      term.addEventListener('mouseenter', (e) => {
        const definition = e.target.dataset.definition;
        this.showGlossaryCard(e.target, term.textContent, definition);
      });

      term.addEventListener('mouseleave', () => {
        this.hideCard();
      });
    });
  }

  showReferenceCard(element, paperId) {
    clearTimeout(this.currentTimeout);

    this.currentTimeout = setTimeout(() => {
      const isInPaperDir = window.location.pathname.includes('/paper/');
      const base = isInPaperDir ? '../' : '';
      fetch(`${base}paper/${paperId}.json`)
        .then(r => r.json())
        .then(data => {
          const authors = data.authors ? data.authors.join(', ') : 'Unknown';
          this.card.innerHTML = `
            <h4>${data.title || 'Unknown'}</h4>
            <div class="meta">
              ${authors}<br>
              ${data.year || 'N/A'} \u2022 ${data.venue || 'N/A'}<br>
              Citations: ${data.citation_count || 0}
            </div>
            <div class="abstract">${data.abstract || ''}</div>
          `;

          this.positionCard(element);
          this.card.classList.add('visible');
        })
        .catch(err => console.error('Error loading paper:', err));
    }, 300);
  }

  showGlossaryCard(element, term, definition) {
    clearTimeout(this.currentTimeout);

    this.currentTimeout = setTimeout(() => {
      this.card.innerHTML = `
        <h4>${term}</h4>
        <div class="abstract">${definition}</div>
      `;

      this.positionCard(element);
      this.card.classList.add('visible');
    }, 300);
  }

  positionCard(element) {
    const rect = element.getBoundingClientRect();
    const cardWidth = 320;
    const left = Math.min(rect.left, window.innerWidth - cardWidth - 16);
    this.card.style.left = Math.max(8, left) + 'px';
    this.card.style.top = (rect.bottom + 8) + 'px';
  }

  hideCard() {
    this.currentTimeout = setTimeout(() => {
      this.card.classList.remove('visible');
    }, 100);
  }
}

// Search functionality
class Search {
  constructor() {
    this.searchIndex = null;
    this.dropdown = null;
    this.activeIndex = -1;
    this.input = document.getElementById('search');
    if (!this.input) return;
    this.init();
  }

  async init() {
    const isInPaperDir = window.location.pathname.includes('/paper/');
    const basePath = isInPaperDir ? '../' : '';
    try {
      const response = await fetch(`${basePath}search_index.json`);
      this.searchIndex = await response.json();
    } catch (err) {
      console.error('Failed to load search index:', err);
    }
    this.createDropdown();
    this.bindEvents();
  }

  createDropdown() {
    this.dropdown = document.createElement('div');
    this.dropdown.className = 'search-dropdown';
    this.input.parentElement.appendChild(this.dropdown);
  }

  bindEvents() {
    this.input.addEventListener('input', () => {
      this.activeIndex = -1;
      const q = this.input.value.trim();
      if (q.length < 2) { this.hide(); return; }
      this.render(this.search(q), q);
    });

    this.input.addEventListener('keydown', (e) => {
      const items = this.dropdown.querySelectorAll('.search-result');
      if (e.key === 'Escape') { this.hide(); this.input.blur(); return; }
      if (!items.length) return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        this.setActive(Math.min(this.activeIndex + 1, items.length - 1), items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        this.setActive(Math.max(this.activeIndex - 1, 0), items);
      } else if (e.key === 'Enter' && this.activeIndex >= 0) {
        e.preventDefault();
        items[this.activeIndex].click();
      }
    });

    document.addEventListener('click', (e) => {
      if (!this.input.parentElement.contains(e.target)) this.hide();
    });
  }

  setActive(idx, items) {
    items.forEach(el => el.classList.remove('active'));
    this.activeIndex = idx;
    items[idx].classList.add('active');
    items[idx].scrollIntoView({ block: 'nearest' });
  }

  search(query) {
    if (!this.searchIndex) return [];
    const q = query.toLowerCase();
    return this.searchIndex.filter(p =>
      p.title.toLowerCase().includes(q) ||
      (p.authors && p.authors.join(' ').toLowerCase().includes(q)) ||
      (p.venue && p.venue.toLowerCase().includes(q)) ||
      (p.tags && p.tags.join(' ').toLowerCase().includes(q)) ||
      (p.content && p.content.toLowerCase().includes(q))
    ).slice(0, 8);
  }

  highlight(text, query) {
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    return text.slice(0, idx)
      + `<mark>${text.slice(idx, idx + query.length)}</mark>`
      + text.slice(idx + query.length);
  }

  render(results, query) {
    const isInPaperDir = window.location.pathname.includes('/paper/');
    const base = isInPaperDir ? '../' : '';

    if (!results.length) {
      this.dropdown.innerHTML = '<div class="search-no-results">No papers found</div>';
      this.dropdown.classList.add('visible');
      return;
    }

    const countHeader = `<div class="search-result-count">${results.length} result${results.length !== 1 ? 's' : ''}</div>`;

    const items = results.map(p => {
      const authors = p.authors
        ? p.authors.slice(0, 2).join(', ') + (p.authors.length > 2 ? ' et al.' : '')
        : '';
      const tags = (p.tags || []).slice(0, 3)
        .map(t => `<span class="search-result-tag">${t}</span>`).join('');
      const citations = p.citation_count
        ? `<span class="search-result-citations">📖 ${p.citation_count.toLocaleString()}</span>`
        : '';
      const metaParts = [
        authors ? `<span>${authors}</span>` : '',
        p.year   ? `<span class="year">${p.year}</span>` : '',
        p.venue  ? `<span>${p.venue}</span>` : '',
      ].filter(Boolean).join('<span class="sep">\u2022</span>');

      return `<div class="search-result" onclick="window.location.href='${base}paper/${p.paper_id}.html'">
        <div class="search-result-title">${this.highlight(p.title, query)}</div>
        <div class="search-result-meta">${metaParts}</div>
        ${(tags || citations) ? `<div class="search-result-footer">
          <div class="search-result-tags">${tags}</div>
          ${citations}
        </div>` : ''}
      </div>`;
    }).join('');

    this.dropdown.innerHTML = countHeader + items;
    this.dropdown.classList.add('visible');
  }

  hide() {
    if (this.dropdown) this.dropdown.classList.remove('visible');
    this.activeIndex = -1;
  }
}

// Reading progress bar
function initProgressBar() {
  const bar = document.querySelector('.reading-progress');
  if (!bar) return;
  function update() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    bar.style.width = pct + '%';
  }
  window.addEventListener('scroll', update, { passive: true });
  update();
}

// Dark mode
function initDarkMode() {
  const btn = document.getElementById('dark-toggle');
  if (!btn) return;

  const saved = localStorage.getItem('wiki-theme');
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    btn.textContent = '☀️ Light';
  } else {
    btn.textContent = '🌙 Dark';
  }

  btn.addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (isDark) {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('wiki-theme', 'light');
      btn.textContent = '🌙 Dark';
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('wiki-theme', 'dark');
      btn.textContent = '☀️ Light';
    }
  });
}

// Index sort + filter controls
function initIndexControls() {
  const grid = document.getElementById('paper-grid');
  if (!grid) return;

  let activeTag = null;

  // Sort
  document.querySelectorAll('.sort-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      sortGrid(btn.dataset.sort);
    });
  });

  function sortGrid(mode) {
    const cards = Array.from(grid.querySelectorAll('.paper-card'));
    cards.sort((a, b) => {
      if (mode === 'newest') return parseInt(b.dataset.year || 0) - parseInt(a.dataset.year || 0);
      if (mode === 'oldest') return parseInt(a.dataset.year || 0) - parseInt(b.dataset.year || 0);
      if (mode === 'az')     return (a.dataset.title || '').localeCompare(b.dataset.title || '');
      // most-cited (default)
      return parseInt(b.dataset.citations || 0) - parseInt(a.dataset.citations || 0);
    });
    cards.forEach(c => grid.appendChild(c));
    updateNoResults();
  }

  // Tag filter via toolbar pills
  document.querySelectorAll('.filter-tag-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tag = btn.dataset.tag;
      if (activeTag === tag) {
        activeTag = null;
        btn.classList.remove('active');
      } else {
        document.querySelectorAll('.filter-tag-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeTag = tag;
      }
      applyFilter();
    });
  });

  // Clear button
  const clearBtn = document.querySelector('.clear-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      activeTag = null;
      document.querySelectorAll('.filter-tag-btn').forEach(b => b.classList.remove('active'));
      applyFilter();
    });
  }

  function applyFilter() {
    const cards = grid.querySelectorAll('.paper-card');
    cards.forEach(card => {
      if (!activeTag) {
        card.classList.remove('hidden');
      } else {
        const tags = (card.dataset.tags || '').split(',').map(t => t.trim());
        if (tags.includes(activeTag)) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      }
    });
    updateNoResults();
  }

  function updateNoResults() {
    let existing = grid.querySelector('.no-results-msg');
    const visible = Array.from(grid.querySelectorAll('.paper-card')).filter(c => !c.classList.contains('hidden'));
    if (visible.length === 0) {
      if (!existing) {
        const msg = document.createElement('div');
        msg.className = 'no-results-msg';
        msg.textContent = 'No papers match the selected filter.';
        grid.appendChild(msg);
      }
    } else if (existing) {
      existing.remove();
    }
  }

  // Random paper button
  const randomBtn = document.querySelector('.random-btn');
  if (randomBtn) {
    randomBtn.addEventListener('click', () => {
      const visible = Array.from(grid.querySelectorAll('.paper-card')).filter(c => !c.classList.contains('hidden'));
      if (!visible.length) return;
      const pick = visible[Math.floor(Math.random() * visible.length)];
      pick.click();
    });
  }

  // Tag cloud in sidebar (filter-tag-btn with data-tag)
  document.querySelectorAll('#tag-cloud .filter-tag-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tag = btn.dataset.tag;
      // sync with toolbar
      const toolbarBtn = document.querySelector(`.index-toolbar .filter-tag-btn[data-tag="${tag}"]`);
      if (toolbarBtn) toolbarBtn.click();
      else {
        if (activeTag === tag) {
          activeTag = null;
          btn.classList.remove('active');
        } else {
          document.querySelectorAll('#tag-cloud .filter-tag-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeTag = tag;
        }
        applyFilter();
      }
    });
  });
}

// Keyboard shortcuts
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
      e.preventDefault();
      const search = document.getElementById('search');
      if (search) search.focus();
    }
  });
}

// Citation Graph (canvas force-directed)
class CitationGraph {
  constructor(canvasId, tooltipId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.tooltip = document.getElementById(tooltipId);
    this.papers = window.PAPERS_DATA || [];
    this.links = window.LINKS_DATA || [];
    this.nodes = [];
    this.edges = [];
    this.dragging = null;
    this.hovering = null;
    this.offsetX = 0;
    this.offsetY = 0;
    this.scale = 1;
    this.isPanning = false;
    this.panStart = null;
    this.panOffsetStart = null;
    this.animFrame = null;

    this.resize();
    this.build();
    this.bindEvents();
    this.simulate();
  }

  resize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width || 800;
    this.canvas.height = Math.max(500, window.innerHeight - 150);
  }

  build() {
    const W = this.canvas.width;
    const H = this.canvas.height;
    const idMap = {};

    this.papers.forEach((p, i) => {
      const node = {
        id: p.paper_id,
        title: p.title,
        year: p.year,
        citations: p.citation_count || 0,
        x: W / 2 + (Math.random() - 0.5) * W * 0.6,
        y: H / 2 + (Math.random() - 0.5) * H * 0.6,
        vx: 0,
        vy: 0,
        r: Math.max(6, Math.min(22, 6 + Math.log1p(p.citation_count || 0) * 1.8)),
      };
      this.nodes.push(node);
      idMap[p.paper_id] = node;
    });

    this.links.forEach(l => {
      const src = idMap[l.source];
      const tgt = idMap[l.target];
      if (src && tgt) this.edges.push({ source: src, target: tgt });
    });
  }

  bindEvents() {
    this.canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
    this.canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
    this.canvas.addEventListener('mouseup', (e) => this.onMouseUp(e));
    this.canvas.addEventListener('mouseleave', () => {
      this.dragging = null;
      this.isPanning = false;
      if (this.tooltip) this.tooltip.classList.remove('visible');
    });
    this.canvas.addEventListener('click', (e) => this.onClick(e));
    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const factor = e.deltaY < 0 ? 1.1 : 0.9;
      this.scale = Math.max(0.2, Math.min(5, this.scale * factor));
    }, { passive: false });
    window.addEventListener('resize', () => { this.resize(); });
  }

  getCanvasPos(e) {
    const rect = this.canvas.getBoundingClientRect();
    return {
      x: (e.clientX - rect.left - this.offsetX) / this.scale,
      y: (e.clientY - rect.top - this.offsetY) / this.scale,
    };
  }

  getScreenPos(e) {
    const rect = this.canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  hitTest(pos) {
    for (let i = this.nodes.length - 1; i >= 0; i--) {
      const n = this.nodes[i];
      const dx = pos.x - n.x;
      const dy = pos.y - n.y;
      if (dx * dx + dy * dy <= n.r * n.r) return n;
    }
    return null;
  }

  onMouseDown(e) {
    const pos = this.getCanvasPos(e);
    const hit = this.hitTest(pos);
    if (hit) {
      this.dragging = hit;
      this.dragging.fixed = true;
    } else {
      this.isPanning = true;
      this.panStart = this.getScreenPos(e);
      this.panOffsetStart = { x: this.offsetX, y: this.offsetY };
    }
  }

  onMouseUp(e) {
    if (this.dragging) { this.dragging.fixed = false; this.dragging = null; }
    this.isPanning = false;
  }

  onMouseMove(e) {
    if (this.dragging) {
      const pos = this.getCanvasPos(e);
      this.dragging.x = pos.x;
      this.dragging.y = pos.y;
      this.dragging.vx = 0;
      this.dragging.vy = 0;
    } else if (this.isPanning && this.panStart) {
      const sp = this.getScreenPos(e);
      this.offsetX = this.panOffsetStart.x + (sp.x - this.panStart.x);
      this.offsetY = this.panOffsetStart.y + (sp.y - this.panStart.y);
    } else {
      const pos = this.getCanvasPos(e);
      const hit = this.hitTest(pos);
      this.hovering = hit;
      if (hit && this.tooltip) {
        this.tooltip.innerHTML = `<strong>${hit.title}</strong><br>${hit.year || 'N/A'} &bull; ${hit.citations.toLocaleString()} citations`;
        this.tooltip.classList.add('visible');
        this.tooltip.style.left = (e.clientX + 14) + 'px';
        this.tooltip.style.top = (e.clientY - 10) + 'px';
      } else if (this.tooltip) {
        this.tooltip.classList.remove('visible');
      }
    }
    this.canvas.style.cursor = this.hovering ? 'pointer' : (this.isPanning ? 'grabbing' : 'grab');
  }

  onClick(e) {
    if (this.isPanning) return;
    const pos = this.getCanvasPos(e);
    const hit = this.hitTest(pos);
    if (hit) {
      const isInPaper = window.location.pathname.includes('/paper/');
      const base = isInPaper ? '../' : '';
      window.location.href = base + 'paper/' + hit.id + '.html';
    }
  }

  simulate() {
    const alpha = { val: 1 };
    const step = () => {
      if (alpha.val > 0.001) {
        this.tick(alpha);
        alpha.val *= 0.995;
      }
      this.draw();
      this.animFrame = requestAnimationFrame(step);
    };
    step();
  }

  tick(alpha) {
    const W = this.canvas.width / this.scale;
    const H = this.canvas.height / this.scale;
    const k = Math.sqrt((W * H) / Math.max(1, this.nodes.length));

    // Repulsion
    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const a = this.nodes[i];
        const b = this.nodes[j];
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
        const force = (k * k) / dist * alpha.val;
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        a.vx -= fx; a.vy -= fy;
        b.vx += fx; b.vy += fy;
      }
    }

    // Attraction along edges
    this.edges.forEach(edge => {
      const dx = edge.target.x - edge.source.x;
      const dy = edge.target.y - edge.source.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
      const force = (dist * dist) / k * alpha.val * 0.3;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      edge.source.vx += fx; edge.source.vy += fy;
      edge.target.vx -= fx; edge.target.vy -= fy;
    });

    // Center gravity
    const cx = W / 2, cy = H / 2;
    this.nodes.forEach(n => {
      if (n.fixed) return;
      n.vx += (cx - n.x) * 0.01 * alpha.val;
      n.vy += (cy - n.y) * 0.01 * alpha.val;
      n.x += n.vx * 0.4;
      n.y += n.vy * 0.4;
      n.vx *= 0.8;
      n.vy *= 0.8;
      // clamp
      n.x = Math.max(n.r, Math.min(W - n.r, n.x));
      n.y = Math.max(n.r, Math.min(H - n.r, n.y));
    });
  }

  draw() {
    const ctx = this.ctx;
    const W = this.canvas.width;
    const H = this.canvas.height;
    ctx.clearRect(0, 0, W, H);
    ctx.save();
    ctx.translate(this.offsetX, this.offsetY);
    ctx.scale(this.scale, this.scale);

    // Edges
    ctx.strokeStyle = '#a2a9b1';
    ctx.lineWidth = 0.8;
    this.edges.forEach(edge => {
      ctx.beginPath();
      ctx.moveTo(edge.source.x, edge.source.y);
      ctx.lineTo(edge.target.x, edge.target.y);
      ctx.stroke();
    });

    // Nodes
    this.nodes.forEach(n => {
      const isHovered = n === this.hovering;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = isHovered ? '#447ff5' : '#3366cc';
      ctx.fill();
      if (isHovered) {
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      // Label for large/hovered nodes
      if (n.r > 10 || isHovered) {
        ctx.fillStyle = '#202122';
        ctx.font = `${isHovered ? 'bold ' : ''}${Math.min(11, n.r * 0.9)}px sans-serif`;
        ctx.textAlign = 'center';
        const label = n.title.length > 30 ? n.title.slice(0, 28) + '...' : n.title;
        ctx.fillText(label, n.x, n.y + n.r + 12);
      }
    });

    ctx.restore();
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  new HoverCard();
  new Search();
  initProgressBar();
  initDarkMode();
  initIndexControls();
  initKeyboardShortcuts();
  if (window.PAPERS_DATA) {
    new CitationGraph('graph-canvas', 'graph-tooltip');
  }
});
"""

    with open(SITE_DIR / "assets" / "js" / "wiki.js", 'w', encoding='utf-8') as f:
        f.write(js_content)


def generate_index(papers, glossary):
    """Generate index.html - main landing page."""
    # Collect all unique tags
    all_tags = []
    seen = set()
    for paper in papers:
        for tag in paper.get('tags', []):
            if tag not in seen:
                all_tags.append(tag)
                seen.add(tag)
    all_tags.sort()

    # Build toolbar pills HTML
    tag_pills_html = ''
    for tag in all_tags:
        tag_pills_html += f'<button class="filter-tag-btn" data-tag="{tag}">{tag}</button>\n        '

    # Build tag cloud for sidebar
    tag_cloud_html = ''
    for tag in all_tags:
        tag_cloud_html += f'<button class="filter-tag-btn" data-tag="{tag}" style="display:block;width:100%;text-align:left;margin-bottom:0.25rem;">{tag}</button>\n        '

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Research Wiki - Knowledge Base</title>
  <link rel="stylesheet" href="assets/css/wiki.css">
</head>
<body>
  <header class="wiki-header">
    <a href="index.html" class="wiki-logo">&#128218; Research Wiki</a>
    <div class="wiki-search">
      <input type="text" id="search" placeholder="Search papers..." autocomplete="off">
    </div>
    <nav class="wiki-nav">
      <a href="timeline.html">Timeline</a>
      <a href="graph.html">Citation Graph</a>
      <button class="dark-toggle" id="dark-toggle">&#9790; Dark</button>
    </nav>
  </header>

  <main class="wiki-content">
    <aside class="wiki-sidebar">
      <h3>Quick Stats</h3>
      <ul>
        <li>{len(papers)} Papers</li>
        <li>{len(glossary)} Glossary Terms</li>
        <li>{sum(p.get('citation_count', 0) for p in papers)} Total Citations</li>
      </ul>

      <h3 style="margin-top: 1.5rem;">Tags</h3>
      <div id="tag-cloud">
        {tag_cloud_html}
      </div>
    </aside>

    <article class="wiki-article">
      <h1>Research Wiki</h1>
      <p>Welcome to your interactive research knowledge base. Explore papers, concepts, and their connections.</p>

      <h2>Papers</h2>

      <div class="index-toolbar">
        <span class="toolbar-label">Sort:</span>
        <button class="sort-btn active" data-sort="most-cited">Most Cited</button>
        <button class="sort-btn" data-sort="newest">Newest</button>
        <button class="sort-btn" data-sort="oldest">Oldest</button>
        <button class="sort-btn" data-sort="az">A&#8211;Z</button>
        <div class="toolbar-sep"></div>
        <span class="toolbar-label">Filter:</span>
        {tag_pills_html}
        <button class="clear-btn">Clear</button>
        <button class="random-btn">&#127922; Random Paper</button>
      </div>

      <div class="paper-grid" id="paper-grid">
"""

    for paper in papers:
        authors = ', '.join(paper['authors'][:3]) if paper['authors'] else 'Unknown'
        if len(paper.get('authors', [])) > 3:
            authors += ' et al.'

        tags_html = ''
        for tag in paper.get('tags', [])[:3]:
            tags_html += f'<span class="tag" style="background: #e3f2fd; color: #1976d2;">{tag}</span>'

        tags_data = ','.join(paper.get('tags', []))
        year_val = paper.get('year') or 0
        citations_val = paper.get('citation_count') or 0
        title_val = paper['title'].replace('"', '&quot;')

        html += f"""
        <div class="paper-card" onclick="window.location.href='paper/{paper['paper_id']}.html'"
             data-year="{year_val}" data-citations="{citations_val}"
             data-title="{title_val}" data-tags="{tags_data}">
          <h3>{paper['title']}</h3>
          <div class="authors">{authors}</div>
          <div class="meta">
            <span>{paper['year'] or 'N/A'} &bull; {paper['venue'] or 'N/A'}</span>
            <span class="citations">&#128218; {paper['citation_count'] or 0} citations</span>
          </div>
          <div>{tags_html}</div>
        </div>
"""

    html += """
      </div>
    </article>
  </main>

  <footer class="wiki-footer">
    <p>Research Wiki Knowledge Base &bull; Built with &#9829; for scientific discovery</p>
  </footer>

  <script src="assets/js/wiki.js"></script>
</body>
</html>"""

    with open(SITE_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ Generated index.html ({len(papers)} papers)")


def generate_paper_page(paper, glossary):
    """Generate individual paper page with rich Wikipedia features."""
    paper_id = paper['paper_id']

    # Create glossary HTML
    glossary_dict = {g['term'].lower(): g['definition'] for g in glossary}

    # Authors
    authors_html = ', '.join(paper['authors'])

    # Tags
    tags_html = ''
    for tag_info in paper.get('tag_details', []):
        tags_html += f'<span class="tag" style="background: {tag_info["color"]}20; color: {tag_info["color"]};">{tag_info["tag"]}</span>'
    # Fallback to plain tags if tag_details empty
    if not tags_html:
        for tag in paper.get('tags', []):
            tags_html += f'<span class="tag" style="background: #e3f2fd; color: #1976d2;">{tag}</span>'

    # Helper to get figure by index
    def get_fig(idx):
        if not idx: return None
        for f in paper.get('figures', []):
            if f.get('figure_index') == idx: return f
        return None

    # Helper to get figure explanation
    def get_fig_expl(idx):
        for fe in paper.get('figure_explanations', []):
            if fe.get('figure_index') == idx: return fe.get('explanation', '')
        return ''

    # Infobox Data
    infobox_html = f"""
      <div class="infobox">
        <div class="infobox-title">{paper.get('main_concept', 'Paper Details')}</div>
"""
    main_img = None
    if paper.get('animation_path'):
        main_img = f"../assets/{paper['animation_path']}"
    elif paper.get('figures'):
        main_img = f"../assets/figures/{paper['figures'][0]['filename']}"

    if main_img:
        infobox_html += f'        <div class="infobox-image"><img src="{main_img}" alt="Concept"></div>\n'

    infobox_html += "        <table>\n"
    ib_data = paper.get('infobox_data', {})
    if isinstance(ib_data, dict):
        for label, value in ib_data.items():
            nice_label = label.replace('_', ' ').title()
            infobox_html += f"          <tr><th>{nice_label}</th><td>{value}</td></tr>\n"

    infobox_html += f"""
          <tr><th>Venue</th><td>{paper['venue'] or 'N/A'}</td></tr>
          <tr><th>Year</th><td>{paper['year'] or 'N/A'}</td></tr>
          <tr><th>Citations</th><td>{paper['citation_count'] or 0}</td></tr>
          <tr><th>DOI</th><td><a href="https://doi.org/{paper.get('doi', '')}" target="_blank">Link</a></td></tr>
        </table>
      </div>
"""

    # Sidebar / Contents
    has_cited_by = bool(paper.get('cited_by'))
    has_related = bool(paper.get('related'))

    sidebar_html = """
    <aside class="wiki-sidebar">
      <h3>Contents</h3>
      <ul>
        <li><a href="#title">Top</a></li>
"""
    for i, section in enumerate(paper.get('sections', [])):
        sidebar_html += f'        <li><a href="#section-{i}">{section["title"]}</a></li>\n'

    if paper.get('concept_breakdown'): sidebar_html += '        <li><a href="#concepts">Concepts</a></li>\n'
    if paper.get('math_equations'): sidebar_html += '        <li><a href="#math">Mathematics</a></li>\n'
    if paper.get('figures'): sidebar_html += '        <li><a href="#figures">Figures</a></li>\n'
    if paper.get('see_also'): sidebar_html += '        <li><a href="#see-also">See Also</a></li>\n'
    if paper.get('references'): sidebar_html += '        <li><a href="#references">References</a></li>\n'
    if has_cited_by: sidebar_html += '        <li><a href="#cited-by">Cited By</a></li>\n'
    if has_related: sidebar_html += '        <li><a href="#related">Related Papers</a></li>\n'

    sidebar_html += f"""
      </ul>
      <h3 style="margin-top: 1.5rem;">Tags</h3>
      <div>{tags_html}</div>
    </aside>
"""

    # Article Content
    article_html = f"""
    <article class="wiki-article">
      <h1 id="title">{paper['title']}</h1>

      {infobox_html}

      <p class="lead">{link_glossary_terms(paper.get('lead_paragraph', paper.get('tldr', '')), glossary_dict)}</p>
"""

    # Sections with floating figures
    for i, section in enumerate(paper.get('sections', [])):
        article_html += f'<h2 id="section-{i}">{section["title"]}</h2>\n'

        fig = get_fig(section.get('figure_index'))
        if fig:
            article_html += f"""
      <div class="thumb tright">
        <div class="thumbinner">
          <a href="../assets/figures/{fig['filename']}" target="_blank">
            <img src="../assets/figures/{fig['filename']}" class="thumbimage" alt="Figure {fig['figure_index']}">
          </a>
          <div class="thumbcaption">
            <b>Figure {fig['figure_index']}:</b> {fig.get('caption', '')}
          </div>
        </div>
      </div>
"""

        paragraphs = section['content'].split('\n\n')
        for p in paragraphs:
            p_processed = re.sub(r'\[\[Figure (\d+)\]\]', r'<b>Figure \1</b>', p)
            article_html += f'<p>{link_glossary_terms(p_processed, glossary_dict)}</p>\n'

    # Concept Breakdown
    if paper.get('concept_breakdown'):
        article_html += '<h2 id="concepts">Concept Breakdown</h2>\n'
        for item in paper['concept_breakdown']:
            article_html += f"""
      <div class="concept-item">
        <div class="concept-title">{item['concept']}</div>
        <p>{link_glossary_terms(item['description'], glossary_dict)}</p>
      </div>
"""

    # Math Equations
    if paper.get('math_equations'):
        article_html += '<h2 id="math">Mathematics</h2>\n'
        for eq in paper['math_equations']:
            article_html += f'<h3>{eq.get("name", "Equation")}</h3>\n'
            article_html += f'<div class="math-block">$${eq.get("latex", "")}$$</div>\n'
            article_html += f'<div class="math-explanation-box">{link_glossary_terms(eq.get("explanation", ""), glossary_dict)}'

            if eq.get('symbols'):
                article_html += '<table class="symbol-table"><tr><th>Symbol</th><th>Meaning</th></tr>'
                for s in eq['symbols']:
                    article_html += f'<tr><td>${s["symbol"]}$</td><td>{s["meaning"]}</td></tr>'
                article_html += '</table>'

            article_html += '</div>\n'

    # All Figures Gallery
    if paper.get('figures'):
        article_html += '<h2 id="figures">Figures and Explanations</h2>\n'
        for fig in paper['figures']:
            expl = get_fig_expl(fig['figure_index'])
            article_html += f"""
      <div class="thumb" style="float:none; width:100%; margin: 1rem 0;">
        <div class="thumbinner" style="width:100%;">
          <img src="../assets/figures/{fig['filename']}" style="max-height: 400px;">
          <div class="thumbcaption">
            <b>Figure {fig['figure_index']}:</b> {fig.get('caption', '')}<br>
            <hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #ddd;">
            {expl}
          </div>
        </div>
      </div>
"""

    # See Also
    if paper.get('see_also'):
        article_html += '<h2 id="see-also">See Also</h2>\n<div class="see-also-grid">'
        for item in paper['see_also']:
            article_html += f"""
        <div class="see-also-item">
          <b>{item['topic']}</b>
          <span style="font-size: 0.8rem; color: #54595d;">{item['description']}</span>
        </div>
"""
        article_html += '</div>\n'

    # References
    if paper.get('references'):
        article_html += """
      <h2 id="references">References</h2>
      <ol class="reference-list">
"""
        for ref in paper.get('references', []):
            ref_authors = json.loads(ref['authors']) if isinstance(ref['authors'], str) else ref.get('authors', [])
            authors_str = ', '.join(ref_authors[:2]) if ref_authors else 'Unknown'
            if len(ref_authors) > 2: authors_str += ' et al.'

            paper_id_attr = f'data-paper-id="{ref["cited_paper_id"]}"' if ref.get('cited_paper_id') else ''

            article_html += f"""
        <li class="reference-item">
          <a class="reference-link" {paper_id_attr}>{ref.get('title', 'Untitled')}</a>
          <span style="font-size: 0.8rem; color: #54595d;"> - {authors_str} ({ref.get('year', 'N/A')})</span>
        </li>
"""
        article_html += "      </ol>\n"

    # Cited By section
    if has_cited_by:
        article_html += '<h2 id="cited-by">Cited By</h2>\n<div class="related-grid">\n'
        for cb in paper['cited_by']:
            cb_title = cb.get('title', 'Untitled')
            cb_year = cb.get('year', 'N/A')
            cb_cit = cb.get('citation_count', 0)
            cb_id = cb.get('paper_id', '')
            article_html += f"""  <div class="related-card" onclick="window.location.href='..//paper/{cb_id}.html'">
    <div class="related-card-title">{cb_title}</div>
    <div class="related-card-meta">{cb_year} &bull; {cb_cit} citations</div>
  </div>
"""
        article_html += '</div>\n'

    # Related Papers section
    if has_related:
        article_html += '<h2 id="related">Related Papers</h2>\n<div class="related-grid">\n'
        for rel in paper['related']:
            rel_title = rel.get('title', 'Untitled')
            rel_year = rel.get('year', 'N/A')
            rel_cit = rel.get('citation_count', 0)
            rel_id = rel.get('paper_id', '')
            article_html += f"""  <div class="related-card" onclick="window.location.href='../paper/{rel_id}.html'">
    <div class="related-card-title">{rel_title}</div>
    <div class="related-card-meta">{rel_year} &bull; {rel_cit} citations</div>
  </div>
"""
        article_html += '</div>\n'

    article_html += "</article>\n"

    # Full Page Assembly
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{paper['title']} - Research Wiki</title>
  <link rel="stylesheet" href="../assets/css/wiki.css">
  <link rel="icon" type="image/png" href="../assets/images/favicon.png">
</head>
<body>
  <div class="reading-progress"></div>
  <header class="wiki-header">
    <a href="../index.html" class="wiki-logo">&#128218; Research Wiki</a>
    <div class="wiki-search">
      <input type="text" id="search" placeholder="Search papers..." autocomplete="off">
    </div>
    <nav class="wiki-nav">
      <a href="../timeline.html">Timeline</a>
      <a href="../graph.html">Citation Graph</a>
      <button class="dark-toggle" id="dark-toggle">&#9790; Dark</button>
    </nav>
  </header>

  <main class="wiki-content">
    {sidebar_html}
    {article_html}
  </main>

  <footer class="wiki-footer">
    <p>This page was generated by Research Wiki. Text is available under the Creative Commons Attribution-ShareAlike License.</p>
  </footer>

  <script src="../assets/js/wiki.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</body>
</html>"""

    with open(SITE_DIR / "paper" / f"{paper_id}.html", 'w', encoding='utf-8') as f:
        f.write(html)

    # Generate JSON for hover cards
    paper_json = {
        'title': paper['title'],
        'authors': paper['authors'],
        'year': paper['year'],
        'venue': paper['venue'],
        'abstract': paper.get('abstract', ''),
        'citation_count': paper.get('citation_count', 0)
    }

    with open(SITE_DIR / "paper" / f"{paper_id}.json", 'w') as f:
        json.dump(paper_json, f)

    print(f"  ✓ Generated {paper_id}.html")


def link_glossary_terms(text, glossary_dict):
    """Link glossary terms in text while avoiding double-wrapping and escaping definitions."""
    import html
    if not text:
        return ""
    
    # Sort terms by length descending to match longest terms first
    sorted_terms = sorted(glossary_dict.items(), key=lambda x: -len(x[0]))
    
    # We want to find matches but avoid replacing inside existing HTML tags
    # or replacing something we already replaced.
    # A simple way is to use a placeholder.
    placeholders = {}
    
    result = text
    
    for term, definition in sorted_terms:
        if not term: continue
        # Use word boundaries if possible to avoid matching substrings of words
        # but be careful with technical terms that might have special chars
        escaped_term = re.escape(term)
        pattern = re.compile(rf"\b({escaped_term})\b", re.IGNORECASE)
        
        # We need to be careful not to match inside an already replaced span
        # Find all matches that are NOT inside a <span ...>...</span>
        
        def replace_with_placeholder(match):
            term_text = match.group(1)
            # Escape the definition for use in HTML attribute
            safe_definition = html.escape(definition).replace('"', '&quot;')
            placeholder = f"__GLOSSARY_{len(placeholders)}__"
            placeholders[placeholder] = f'<span class="glossary-term" data-definition="{safe_definition}">{term_text}</span>'
            return placeholder

        # This is still a bit naive because it might match inside existing HTML
        # if the text already has some (like Figures).
        # Let's use a more robust approach: split by tags, replace in text parts.
        
        parts = re.split(r'(<[^>]+>)', result)
        for i in range(len(parts)):
            if not parts[i].startswith('<'):
                parts[i] = pattern.sub(replace_with_placeholder, parts[i])
        result = ''.join(parts)
        
    # Finally, replace placeholders back
    for placeholder, span in placeholders.items():
        result = result.replace(placeholder, span)
        
    return result


def generate_search_index(papers, conn):
    """Generate search index JSON with full-text content for search."""
    search_index = []
    for paper_basic in papers:
        paper = get_paper(conn, paper_basic['paper_id'])

        content_parts = []
        if paper.get('lead_paragraph'):
            content_parts.append(paper['lead_paragraph'])
        for section in paper.get('sections', []):
            if section.get('title'):
                content_parts.append(section['title'])
            if section.get('content'):
                content_parts.append(section['content'][:500])
        for concept in paper.get('concept_breakdown', []):
            if concept.get('concept'):
                content_parts.append(concept['concept'])
            if concept.get('description'):
                content_parts.append(concept['description'][:200])
        for gt in paper.get('glossary_terms', []):
            if gt.get('term'):
                content_parts.append(gt['term'])

        search_index.append({
            'paper_id': paper['paper_id'],
            'title': paper['title'],
            'authors': paper['authors'],
            'year': paper.get('year'),
            'venue': paper.get('venue'),
            'citation_count': paper.get('citation_count', 0),
            'tags': paper.get('tags', []),
            'content': ' '.join(content_parts)[:3000],
        })

    with open(SITE_DIR / "search_index.json", 'w') as f:
        json.dump(search_index, f, indent=2)

    print(f"  ✓ Generated search_index.json ({len(search_index)} entries)")


def generate_timeline(papers):
    """Generate timeline.html — papers grouped by year in descending order."""
    from collections import defaultdict
    by_year = defaultdict(list)
    for p in papers:
        year = p.get('year') or 0
        by_year[year].append(p)

    years_sorted = sorted(by_year.keys(), reverse=True)

    groups_html = ''
    for year in years_sorted:
        year_papers = by_year[year]
        year_label = str(year) if year else 'Unknown'
        papers_html = ''
        for p in year_papers:
            authors = ', '.join(p['authors'][:2]) if p['authors'] else 'Unknown'
            if len(p.get('authors', [])) > 2:
                authors += ' et al.'
            citations = p.get('citation_count') or 0
            papers_html += f"""
      <div class="timeline-paper" onclick="window.location.href='paper/{p['paper_id']}.html'">
        <div class="timeline-paper-title">{p['title']}</div>
        <div class="timeline-paper-meta">{authors} &bull; {p.get('venue') or 'N/A'} &bull; {citations} citations</div>
      </div>"""

        groups_html += f"""
  <div class="timeline-group">
    <div class="timeline-year-label">{year_label}</div>
    <div class="timeline-papers">{papers_html}
    </div>
  </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Timeline - Research Wiki</title>
  <link rel="stylesheet" href="assets/css/wiki.css">
</head>
<body>
  <header class="wiki-header">
    <a href="index.html" class="wiki-logo">&#128218; Research Wiki</a>
    <div class="wiki-search">
      <input type="text" id="search" placeholder="Search papers..." autocomplete="off">
    </div>
    <nav class="wiki-nav">
      <a href="index.html">Home</a>
      <a href="graph.html">Citation Graph</a>
      <button class="dark-toggle" id="dark-toggle">&#9790; Dark</button>
    </nav>
  </header>

  <div class="timeline-page">
    <h1 style="margin-bottom: 1.5rem; font-family: 'Linux Libertine', Georgia, serif; font-weight: normal;">Paper Timeline</h1>
    {groups_html}
  </div>

  <footer class="wiki-footer">
    <p>Research Wiki Knowledge Base &bull; {len(papers)} papers across {len(years_sorted)} years</p>
  </footer>

  <script src="assets/js/wiki.js"></script>
</body>
</html>"""

    with open(SITE_DIR / "timeline.html", 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ Generated timeline.html ({len(papers)} papers, {len(years_sorted)} years)")


def generate_graph(papers, conn):
    """Generate graph.html — citation graph page."""
    papers_data = [
        {
            'paper_id': p['paper_id'],
            'title': p['title'],
            'year': p.get('year'),
            'citation_count': p.get('citation_count', 0),
        }
        for p in papers
    ]

    # Build links from cross_references
    cursor = conn.cursor()
    cursor.execute("SELECT from_paper_id, to_paper_id FROM cross_references WHERE relationship_type = 'cites'")
    rows = cursor.fetchall()
    paper_ids = {p['paper_id'] for p in papers}
    links_data = [
        {'source': row[0], 'target': row[1]}
        for row in rows
        if row[0] in paper_ids and row[1] in paper_ids
    ]

    papers_json = json.dumps(papers_data)
    links_json = json.dumps(links_data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Citation Graph - Research Wiki</title>
  <link rel="stylesheet" href="assets/css/wiki.css">
</head>
<body>
  <header class="wiki-header">
    <a href="index.html" class="wiki-logo">&#128218; Research Wiki</a>
    <div class="wiki-search">
      <input type="text" id="search" placeholder="Search papers..." autocomplete="off">
    </div>
    <nav class="wiki-nav">
      <a href="index.html">Home</a>
      <a href="timeline.html">Timeline</a>
      <button class="dark-toggle" id="dark-toggle">&#9790; Dark</button>
    </nav>
  </header>

  <div style="padding: 1rem 2rem 0;">
    <h1 style="font-family: 'Linux Libertine', Georgia, serif; font-weight: normal; margin-bottom: 0.3rem;">Citation Graph</h1>
    <p class="graph-hint">Drag nodes to rearrange &bull; Scroll to zoom &bull; Click a node to open paper &bull; {len(papers_data)} papers, {len(links_data)} citation links</p>
  </div>

  <div style="padding: 0 2rem 1rem;">
    <canvas id="graph-canvas"></canvas>
    <div class="graph-tooltip" id="graph-tooltip"></div>
  </div>

  <footer class="wiki-footer">
    <p>Research Wiki Knowledge Base &bull; Citation graph</p>
  </footer>

  <script>
    window.PAPERS_DATA = {papers_json};
    window.LINKS_DATA = {links_json};
  </script>
  <script src="assets/js/wiki.js"></script>
</body>
</html>"""

    with open(SITE_DIR / "graph.html", 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ Generated graph.html ({len(papers_data)} nodes, {len(links_data)} edges)")
