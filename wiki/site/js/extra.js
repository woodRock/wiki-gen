// Citation Hover Cards
(function() {
    // Create the card element
    const card = document.createElement('div');
    card.className = 'cite-card';
    document.body.appendChild(card);
    let citeTimer;

    function escHtml(str) {
        if (!str) return '';
        const d = document.createElement('div');
        d.appendChild(document.createTextNode(str));
        return d.innerHTML;
    }

    function positionCard(el) {
        const rect = el.getBoundingClientRect();
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        const cardRect = card.getBoundingClientRect();
        
        let left = rect.left;
        let top = rect.bottom + 8;

        // Keep on screen horizontally
        if (left + 320 > vw - 10) left = vw - 330;
        if (left < 10) left = 10;

        // Flip above if goes off screen bottom
        if (top + cardRect.height > vh - 10) {
            top = rect.top - cardRect.height - 8;
        }

        card.style.left = left + 'px';
        card.style.top = top + 'px';
    }

    // Delegate hover event for all links that look like citations or references
    document.addEventListener('mouseover', function(e) {
        const el = e.target.closest('a');
        if (!el) return;

        // Check if this is a link to another paper in our wiki
        // Our paper IDs are typically 40 chars long (hex)
        const href = el.getAttribute('href') || '';
        const match = href.match(/([a-f0-9]{40})\.md$/) || href.match(/([a-f0-9]{40})\/?$/);
        
        if (match) {
            const paperId = match[1];
            const meta = (window.PAPERS_META || {})[paperId];
            
            if (meta) {
                clearTimeout(citeTimer);
                card.innerHTML = `
                    <div class="cite-card-title">${escHtml(meta.title)}</div>
                    <div class="cite-card-authors">${escHtml(meta.authors)}</div>
                    <div class="cite-card-meta">
                        ${meta.year ? `<span>${meta.year}</span>` : ''} 
                        ${meta.venue ? ` | <span>${meta.venue}</span>` : ''}
                        ${meta.cc ? ` | <span>${meta.cc} citations</span>` : ''}
                    </div>
                    ${meta.abstract ? `<div class="cite-card-abstract">${escHtml(meta.abstract)}</div>` : ''}
                `;
                
                card.classList.add('visible');
                positionCard(el);
            }
        }
    });

    document.addEventListener('mouseout', function(e) {
        const el = e.target.closest('a');
        if (!el) return;
        
        citeTimer = setTimeout(() => {
            card.classList.remove('visible');
        }, 300);
    });

    // Keep card visible if hovering the card itself
    card.addEventListener('mouseover', () => clearTimeout(citeTimer));
    card.addEventListener('mouseout', () => {
        citeTimer = setTimeout(() => card.classList.remove('visible'), 300);
    });
})();
