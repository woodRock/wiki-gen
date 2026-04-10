
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
      ].filter(Boolean).join('<span class="sep">•</span>');

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

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  new HoverCard();
  new Search();
});
