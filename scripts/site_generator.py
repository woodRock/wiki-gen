"""
Generate Wikipedia-style static HTML site from SQLite database.
"""

import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from db_setup import get_connection, get_all_papers, get_paper, get_glossary

SITE_DIR = Path("wiki/site")
TEMPLATES_DIR = Path("wiki/templates")

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
    
    # Generate index page
    papers = get_all_papers(conn)
    glossary = get_glossary(conn)
    generate_index(papers, glossary)
    
    # Generate individual paper pages
    for paper_data in papers:
        paper = get_paper(conn, paper_data['paper_id'])
        generate_paper_page(paper, glossary)
    
    # Generate search index
    generate_search_index(papers, conn)
    
    conn.close()
    print(f"✅ Generated site in {SITE_DIR}")

def copy_assets():
    """Copy CSS and JS files."""
    # Main CSS
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

/* Search dropdown */
.wiki-search {
  position: relative;
}

.search-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--wiki-border);
  border-top: none;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0,0,0,0.12);
}

.search-dropdown.visible {
  display: block;
}

.search-result {
  padding: 0.6rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.search-result:hover {
  background: var(--wiki-gray-bg);
}

.search-result:last-child {
  border-bottom: none;
}

.search-result-title {
  font-weight: 500;
  color: var(--wiki-link);
  font-size: 0.9rem;
  line-height: 1.3;
}

.search-result-meta {
  font-size: 0.75rem;
  color: #54595d;
  margin-top: 0.15rem;
}

.search-result-tags {
  margin-top: 0.2rem;
}

.search-result-tag {
  display: inline-block;
  padding: 0.1rem 0.35rem;
  margin: 0 0.1rem 0 0;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 2px;
  font-size: 0.7rem;
}

.search-no-results {
  padding: 0.8rem 1rem;
  color: #54595d;
  font-size: 0.85rem;
  font-style: italic;
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
    
    with open(SITE_DIR / "assets" / "css" / "wiki.css", 'w') as f:
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
      // Load paper data
      fetch(`/paper/${paperId}.json`)
        .then(r => r.json())
        .then(data => {
          const authors = data.authors ? data.authors.join(', ') : 'Unknown';
          this.card.innerHTML = `
            <h4>${data.title || 'Unknown'}</h4>
            <div class="meta">
              ${authors}<br>
              ${data.year || 'N/A'} • ${data.venue || 'N/A'}<br>
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
    this.card.style.left = rect.left + 'px';
    this.card.style.top = (rect.bottom + 10) + 'px';
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
    this.input = document.getElementById('search');
    if (!this.input) return;
    this.init();
  }

  async init() {
    // Resolve path relative to current page depth
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
      const q = this.input.value.trim();
      if (q.length < 2) { this.hide(); return; }
      this.render(this.search(q));
    });

    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { this.hide(); this.input.blur(); }
    });

    document.addEventListener('click', (e) => {
      if (!this.input.parentElement.contains(e.target)) this.hide();
    });
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

  render(results) {
    const isInPaperDir = window.location.pathname.includes('/paper/');
    const base = isInPaperDir ? '../' : '';

    if (!results.length) {
      this.dropdown.innerHTML = '<div class="search-no-results">No papers found</div>';
      this.dropdown.classList.add('visible');
      return;
    }

    this.dropdown.innerHTML = results.map(p => {
      const authors = p.authors ? p.authors.slice(0, 2).join(', ') + (p.authors.length > 2 ? ' et al.' : '') : '';
      const tags = (p.tags || []).slice(0, 3).map(t => `<span class="search-result-tag">${t}</span>`).join('');
      return `<div class="search-result" onclick="window.location.href='${base}paper/${p.paper_id}.html'">
        <div class="search-result-title">${p.title}</div>
        <div class="search-result-meta">${[authors, p.year, p.venue].filter(Boolean).join(' \u2022 ')}</div>
        ${tags ? `<div class="search-result-tags">${tags}</div>` : ''}
      </div>`;
    }).join('');

    this.dropdown.classList.add('visible');
  }

  hide() {
    if (this.dropdown) this.dropdown.classList.remove('visible');
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  new HoverCard();
  new Search();
});
"""
    
    with open(SITE_DIR / "assets" / "js" / "wiki.js", 'w') as f:
        f.write(js_content)

def generate_index(papers, glossary):
    """Generate index.html - main landing page."""
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
    <a href="index.html" class="wiki-logo">📚 Research Wiki</a>
    <div class="wiki-search">
      <input type="text" id="search" placeholder="Search papers..." autocomplete="off">
    </div>
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
        <!-- Tags will be populated by JS -->
      </div>
    </aside>
    
    <article class="wiki-article">
      <h1>Research Wiki</h1>
      <p>Welcome to your interactive research knowledge base. Explore papers, concepts, and their connections.</p>
      
      <h2>Papers</h2>
      <div class="paper-grid">
"""
    
    for paper in papers:
        authors = ', '.join(paper['authors'][:3]) if paper['authors'] else 'Unknown'
        if len(paper.get('authors', [])) > 3:
            authors += ' et al.'
        
        tags_html = ''
        for tag in paper.get('tags', [])[:3]:
            tags_html += f'<span class="tag" style="background: #e3f2fd; color: #1976d2;">{tag}</span>'
        
        html += f"""
        <div class="paper-card" onclick="window.location.href='paper/{paper['paper_id']}.html'">
          <h3>{paper['title']}</h3>
          <div class="authors">{authors}</div>
          <div class="meta">
            <span>{paper['year'] or 'N/A'} • {paper['venue'] or 'N/A'}</span>
            <span class="citations">📖 {paper['citation_count'] or 0} citations</span>
          </div>
          <div>{tags_html}</div>
        </div>
"""
    
    html += """
      </div>
    </article>
  </main>
  
  <footer class="wiki-footer">
    <p>Research Wiki Knowledge Base • Built with ♥ for scientific discovery</p>
  </footer>
  
  <script src="assets/js/wiki.js"></script>
</body>
</html>"""
    
    with open(SITE_DIR / "index.html", 'w') as f:
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
    # Use animation as the main infobox image if available, otherwise first figure
    main_img = None
    if paper.get('animation_path'):
        main_img = f"../assets/{paper['animation_path']}"
    elif paper.get('figures'):
        main_img = f"../assets/figures/{paper['figures'][0]['filename']}"
    
    if main_img:
        infobox_html += f'        <div class="infobox-image"><img src="{main_img}" alt="Concept"></div>\n'

    infobox_html += "        <table>\n"
    # Technical fields
    ib_data = paper.get('infobox_data', {})
    if isinstance(ib_data, dict):
        for label, value in ib_data.items():
            nice_label = label.replace('_', ' ').title()
            infobox_html += f"          <tr><th>{nice_label}</th><td>{value}</td></tr>\n"
    
    # Standard fields
    infobox_html += f"""
          <tr><th>Venue</th><td>{paper['venue'] or 'N/A'}</td></tr>
          <tr><th>Year</th><td>{paper['year'] or 'N/A'}</td></tr>
          <tr><th>Citations</th><td>{paper['citation_count'] or 0}</td></tr>
          <tr><th>DOI</th><td><a href="https://doi.org/{paper.get('doi', '')}" target="_blank">Link</a></td></tr>
        </table>
      </div>
"""

    # Sidebar / Contents
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
        
        # Check for figure
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
        
        # Section text
        paragraphs = section['content'].split('\n\n')
        for p in paragraphs:
            # Replace [[Figure X]] tags
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

    # All Figures Gallery (if not already shown)
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
  <header class="wiki-header">
    <a href="../index.html" class="wiki-logo">📚 Research Wiki</a>
    <div class="wiki-search">
      <input type="text" id="search" placeholder="Search papers..." autocomplete="off">
    </div>
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
    
    with open(SITE_DIR / "paper" / f"{paper_id}.html", 'w') as f:
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
    
    with open(SITE_DIR / "paper" / f"{paper_id}.html", 'w') as f:
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
    """Link glossary terms in text."""
    result = text
    for term, definition in sorted(glossary_dict.items(), key=lambda x: -len(x[0])):
        if term.lower() in result.lower():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            replacement = f'<span class="glossary-term" data-definition="{definition}">{term}</span>'
            result = pattern.sub(replacement, result)
    return result

def generate_search_index(papers, conn):
    """Generate search index JSON with full-text content for search."""
    search_index = []
    for paper_basic in papers:
        paper = get_paper(conn, paper_basic['paper_id'])

        # Build searchable text from rich content
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
            'tags': paper.get('tags', []),
            'content': ' '.join(content_parts)[:3000],
        })

    with open(SITE_DIR / "search_index.json", 'w') as f:
        json.dump(search_index, f, indent=2)

    print(f"  ✓ Generated search_index.json ({len(search_index)} entries)")

import re
