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
    generate_search_index(papers, glossary)
    
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: var(--wiki-text);
  background: var(--wiki-bg);
}

/* Header */
.wiki-header {
  background: var(--wiki-gray-bg);
  border-bottom: 1px solid var(--wiki-border);
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.wiki-logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--wiki-text);
  text-decoration: none;
}

.wiki-search {
  flex: 0 1 400px;
}

.wiki-search input {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid var(--wiki-border);
  border-radius: 2px;
  font-size: 0.9rem;
}

/* Main content */
.wiki-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

/* Sidebar */
.wiki-sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
  background: var(--wiki-gray-bg);
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid var(--wiki-border);
}

.wiki-sidebar h3 {
  font-size: 0.9rem;
  text-transform: uppercase;
  color: #54595d;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--wiki-border);
}

.wiki-sidebar ul {
  list-style: none;
}

.wiki-sidebar li {
  margin-bottom: 0.3rem;
}

.wiki-sidebar a {
  color: var(--wiki-link);
  text-decoration: none;
  font-size: 0.9rem;
  display: block;
  padding: 0.3rem 0.5rem;
  border-radius: 2px;
}

.wiki-sidebar a:hover {
  background: var(--wiki-info-bg);
  text-decoration: underline;
}

/* Article */
.wiki-article {
  background: var(--wiki-bg);
}

.wiki-article h1 {
  font-size: 2rem;
  font-weight: normal;
  border-bottom: 1px solid var(--wiki-border);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  font-family: 'Linux Libertine', 'Georgia', 'Times', serif;
}

.wiki-article h2 {
  font-size: 1.5rem;
  font-weight: normal;
  border-bottom: 1px solid var(--wiki-border);
  padding-bottom: 0.3rem;
  margin: 1.5rem 0 1rem;
  font-family: 'Linux Libertine', 'Georgia', 'Times', serif;
}

.wiki-article h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 1.5rem 0 0.5rem;
}

.wiki-article p {
  margin-bottom: 1rem;
}

.wiki-article a {
  color: var(--wiki-link);
  text-decoration: none;
}

.wiki-article a:hover {
  text-decoration: underline;
}

/* Paper metadata */
.paper-infobox {
  background: var(--wiki-gray-bg);
  border: 1px solid var(--wiki-border);
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 4px;
}

.paper-infobox table {
  width: 100%;
  border-collapse: collapse;
}

.paper-infobox th {
  text-align: left;
  padding: 0.5rem;
  font-weight: bold;
  width: 150px;
  vertical-align: top;
}

.paper-infobox td {
  padding: 0.5rem;
}

/* Tags */
.tag {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-right: 0.3rem;
  margin-bottom: 0.3rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.tag:hover {
  transform: scale(1.05);
}

/* Figures */
.wiki-figure {
  margin: 1.5rem 0;
  text-align: center;
}

.wiki-figure img {
  max-width: 100%;
  height: auto;
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
}

.wiki-figure figcaption {
  font-size: 0.9rem;
  color: #54595d;
  margin-top: 0.5rem;
  font-style: italic;
}

/* References */
.reference-list {
  list-style: none;
  counter-reset: ref-counter;
}

.reference-item {
  counter-increment: ref-counter;
  margin-bottom: 0.8rem;
  padding-left: 2rem;
  position: relative;
}

.reference-item::before {
  content: counter(ref-counter);
  position: absolute;
  left: 0;
  color: var(--wiki-link);
  font-weight: bold;
  cursor: pointer;
}

.reference-link {
  color: var(--wiki-link);
  text-decoration: none;
  cursor: pointer;
}

.reference-link:hover {
  text-decoration: underline;
}

/* Hover cards */
.hover-card {
  position: fixed;
  background: white;
  border: 1px solid var(--wiki-border);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 1rem;
  max-width: 350px;
  z-index: 1000;
  display: none;
  pointer-events: none;
}

.hover-card.visible {
  display: block;
  pointer-events: auto;
}

.hover-card h4 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: var(--wiki-link);
}

.hover-card .meta {
  font-size: 0.8rem;
  color: #72777d;
  margin-bottom: 0.5rem;
}

.hover-card .abstract {
  font-size: 0.85rem;
  color: var(--wiki-text);
  line-height: 1.4;
}

/* Glossary terms */
.glossary-term {
  border-bottom: 1px dashed var(--wiki-link);
  cursor: help;
  color: var(--wiki-link);
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
  border-radius: 4px;
  padding: 1.5rem;
  transition: box-shadow 0.2s, transform 0.2s;
  cursor: pointer;
}

.paper-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.paper-card h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: var(--wiki-link);
}

.paper-card .authors {
  font-size: 0.85rem;
  color: #54595d;
  margin-bottom: 0.5rem;
}

.paper-card .meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #72777d;
  margin-bottom: 0.5rem;
}

.paper-card .citations {
  color: var(--primary-color);
  font-weight: bold;
}

/* Footer */
.wiki-footer {
  background: var(--wiki-gray-bg);
  border-top: 1px solid var(--wiki-border);
  padding: 2rem;
  text-align: center;
  margin-top: 3rem;
  font-size: 0.9rem;
  color: #54595d;
}

/* Responsive */
@media (max-width: 768px) {
  .wiki-content {
    grid-template-columns: 1fr;
  }
  
  .wiki-sidebar {
    position: static;
  }
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.hover-card.visible {
  animation: fadeIn 0.2s ease-out;
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
    this.init();
  }
  
  async init() {
    try {
      const response = await fetch('/search_index.json');
      this.searchIndex = await response.json();
    } catch (err) {
      console.error('Failed to load search index:', err);
    }
  }
  
  search(query) {
    if (!this.searchIndex) return [];
    
    query = query.toLowerCase();
    return this.searchIndex.filter(paper => 
      paper.title.toLowerCase().includes(query) ||
      (paper.abstract && paper.abstract.toLowerCase().includes(query)) ||
      (paper.authors && paper.authors.join(' ').toLowerCase().includes(query))
    );
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
    """Generate individual paper page with rich features."""
    paper_id = paper['paper_id']
    
    # Create glossary HTML
    glossary_dict = {g['term'].lower(): g['definition'] for g in glossary}
    
    # Build HTML
    authors_html = ', '.join(paper['authors'])
    
    tags_html = ''
    for tag_info in paper.get('tag_details', []):
        tags_html += f'<span class="tag" style="background: {tag_info["color"]}20; color: {tag_info["color"]};">{tag_info["tag"]}</span>'
    
    # Abstract with glossary linking
    abstract_html = link_glossary_terms(paper.get('abstract', ''), glossary_dict)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{paper['title']} - Research Wiki</title>
  <link rel="stylesheet" href="../assets/css/wiki.css">
</head>
<body>
  <header class="wiki-header">
    <a href="../index.html" class="wiki-logo">📚 Research Wiki</a>
    <div class="wiki-search">
      <input type="text" id="search" placeholder="Search papers..." autocomplete="off">
    </div>
  </header>
  
  <main class="wiki-content">
    <aside class="wiki-sidebar">
      <h3>Contents</h3>
      <ul>
        <li><a href="#overview">Overview</a></li>
        <li><a href="#abstract">Abstract</a></li>
"""
    
    if paper.get('figures'):
        html += '        <li><a href="#figures">Figures</a></li>\n'
    
    if paper.get('references'):
        html += '        <li><a href="#references">References</a></li>\n'
    
    if paper.get('cited_by'):
        html += '        <li><a href="#cited-by">Cited By</a></li>\n'
    
    if paper.get('related'):
        html += '        <li><a href="#related">Related Papers</a></li>\n'
    
    html += f"""
      </ul>
      
      <h3 style="margin-top: 1.5rem;">Tags</h3>
      <div>{tags_html}</div>
    </aside>
    
    <article class="wiki-article">
      <h1 id="title">{paper['title']}</h1>
      
      <div class="paper-infobox">
        <table>
          <tr><th>Authors</th><td>{authors_html}</td></tr>
          <tr><th>Year</th><td>{paper['year'] or 'N/A'}</td></tr>
          <tr><th>Venue</th><td>{paper['venue'] or 'N/A'}</td></tr>
          <tr><th>Citations</th><td><strong>{paper['citation_count'] or 0}</strong> ({paper['influential_citation_count'] or 0} influential)</td></tr>
          <tr><th>DOI</th><td><a href="https://doi.org/{paper.get('doi', '')}" target="_blank">{paper.get('doi', 'N/A')}</a></td></tr>
        </table>
      </div>
      
      <h2 id="overview">Overview</h2>
      <p>{paper.get('tldr', 'N/A')}</p>
      
      <h2 id="abstract">Abstract</h2>
      <p>{abstract_html}</p>
"""
    
    # Figures
    if paper.get('figures'):
        html += """
      <h2 id="figures">Figures and Diagrams</h2>
"""
        for fig in paper['figures']:
            caption = fig.get('caption', f'Figure {fig["figure_index"]}')
            html += f"""
      <figure class="wiki-figure">
        <img src="../assets/figures/{fig['filename']}" alt="{caption}">
        <figcaption>{caption}</figcaption>
      </figure>
"""
    
    # References
    if paper.get('references'):
        html += """
      <h2 id="references">References</h2>
      <ol class="reference-list">
"""
        for ref in paper['paper_references'] if 'paper_references' in paper else paper.get('references', []):
            ref_authors = json.loads(ref['authors']) if isinstance(ref['authors'], str) else ref.get('authors', [])
            authors_str = ', '.join(ref_authors[:3]) if ref_authors else 'Unknown'
            if len(ref_authors) > 3:
                authors_str += ' et al.'
            
            paper_id_attr = f'data-paper-id="{ref["cited_paper_id"]}"' if ref.get('cited_paper_id') else ''
            
            html += f"""
        <li class="reference-item">
          <a class="reference-link" {paper_id_attr}>{ref.get('title', 'Untitled')}</a>
          <div style="font-size: 0.85rem; color: #54595d; margin-top: 0.2rem;">
            {authors_str} ({ref.get('year', 'N/A')})
          </div>
        </li>
"""
        html += "      </ol>\n"
    
    # Cited by
    if paper.get('cited_by'):
        html += """
      <h2 id="cited-by">Cited By</h2>
      <ul>
"""
        for citing in paper['cited_by']:
            html += f'        <li><a href="{citing["paper_id"]}.html">{citing["title"]}</a></li>\n'
        html += "      </ul>\n"
    
    # Related papers
    if paper.get('related'):
        html += """
      <h2 id="related">Related Papers</h2>
      <ul>
"""
        for related in paper['related']:
            html += f'        <li><a href="{related["paper_id"]}.html">{related["title"]}</a></li>\n'
        html += "      </ul>\n"
    
    html += """
    </article>
  </main>
  
  <footer class="wiki-footer">
    <p>Research Wiki Knowledge Base • Built with ♥ for scientific discovery</p>
  </footer>
  
  <div class="hover-card"></div>
  <script src="../assets/js/wiki.js"></script>
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

def generate_search_index(papers, glossary):
    """Generate search index JSON."""
    search_index = []
    for paper in papers:
        search_index.append({
            'paper_id': paper['paper_id'],
            'title': paper['title'],
            'authors': paper['authors'],
            'year': paper.get('year'),
            'venue': paper.get('venue'),
            'abstract': paper.get('abstract', '')[:500],
            'tags': paper.get('tags', [])
        })
    
    with open(SITE_DIR / "search_index.json", 'w') as f:
        json.dump(search_index, f, indent=2)
    
    print(f"  ✓ Generated search_index.json ({len(search_index)} entries)")

import re
