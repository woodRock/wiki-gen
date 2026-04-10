
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
