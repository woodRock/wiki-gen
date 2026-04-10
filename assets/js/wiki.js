
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
        <div class="search-result-meta">${[authors, p.year, p.venue].filter(Boolean).join(' • ')}</div>
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
