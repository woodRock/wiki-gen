"""
Database setup and management for Research Wiki Knowledge Base.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("wiki/data/wiki.db")

def get_connection():
    """Get database connection, creating directories if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    """Initialize database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Papers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            paper_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors TEXT,  -- JSON array
            year INTEGER,
            venue TEXT,
            doi TEXT,
            abstract TEXT,
            tldr TEXT,
            citation_count INTEGER DEFAULT 0,
            influential_citation_count INTEGER DEFAULT 0,
            pdf_filename TEXT,
            summary TEXT,  -- Rich HTML summary
            tags TEXT,  -- JSON array
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Figures table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS figures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paper_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            caption TEXT,
            page_num INTEGER,
            figure_index INTEGER,
            FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE
        )
    """)
    
    # Glossary table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS glossary (
            term TEXT PRIMARY KEY,
            definition TEXT NOT NULL,
            paper_id TEXT,
            occurrences TEXT,  -- JSON array of paper_ids
            FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
        )
    """)
    
    # References table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citing_paper_id TEXT NOT NULL,
            cited_paper_id TEXT,
            title TEXT,
            authors TEXT,
            year INTEGER,
            venue TEXT,
            abstract TEXT,
            citation_count INTEGER DEFAULT 0,
            is_in_db BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (citing_paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE
        )
    """)
    
    # Cross-references table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cross_references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_paper_id TEXT NOT NULL,
            to_paper_id TEXT NOT NULL,
            relationship_type TEXT DEFAULT 'cites',
            context TEXT,
            FOREIGN KEY (from_paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE,
            FOREIGN KEY (to_paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE,
            UNIQUE(from_paper_id, to_paper_id, relationship_type)
        )
    """)
    
    # Tags table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            tag TEXT PRIMARY KEY,
            description TEXT,
            color TEXT DEFAULT '#4A90E2'
        )
    """)
    
    # Paper-tags junction table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_tags (
            paper_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            PRIMARY KEY (paper_id, tag),
            FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE,
            FOREIGN KEY (tag) REFERENCES tags(tag) ON DELETE CASCADE
        )
    """)
    
    # Create indexes for faster queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_papers_citations ON papers(citation_count)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_figures_paper ON figures(paper_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_references_citing ON paper_references(citing_paper_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_references_cited ON paper_references(cited_paper_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cross_refs_from ON cross_references(from_paper_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cross_refs_to ON cross_references(to_paper_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_paper_tags_paper ON paper_tags(paper_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_paper_tags_tag ON paper_tags(tag)")
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

def insert_paper(conn, paper_data):
    """Insert or update a paper in the database."""
    cursor = conn.cursor()
    
    authors_json = json.dumps(paper_data.get('authors', []))
    tags_json = json.dumps(paper_data.get('tags', []))
    
    cursor.execute("""
        INSERT OR REPLACE INTO papers 
        (paper_id, title, authors, year, venue, doi, abstract, tldr, 
         citation_count, influential_citation_count, pdf_filename, summary, tags, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        paper_data['paper_id'],
        paper_data['title'],
        authors_json,
        paper_data.get('year'),
        paper_data.get('venue'),
        paper_data.get('doi'),
        paper_data.get('abstract'),
        paper_data.get('tldr'),
        paper_data.get('citation_count', 0),
        paper_data.get('influential_citation_count', 0),
        paper_data.get('pdf_filename'),
        paper_data.get('summary'),
        tags_json
    ))
    
    # Insert tags
    if paper_data.get('tags'):
        for tag in paper_data['tags']:
            cursor.execute("INSERT OR IGNORE INTO tags (tag) VALUES (?)", (tag,))
            cursor.execute("INSERT OR IGNORE INTO paper_tags (paper_id, tag) VALUES (?, ?)",
                         (paper_data['paper_id'], tag))
    
    return paper_data['paper_id']

def insert_figure(conn, paper_id, figure_data):
    """Insert a figure into the database."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO figures (paper_id, filename, caption, page_num, figure_index)
        VALUES (?, ?, ?, ?, ?)
    """, (
        paper_id,
        figure_data['filename'],
        figure_data.get('caption'),
        figure_data.get('page_num'),
        figure_data.get('index')
    ))
    return cursor.lastrowid

def insert_reference(conn, citing_paper_id, ref_data):
    """Insert a reference/citation."""
    cursor = conn.cursor()
    
    authors_json = json.dumps(ref_data.get('authors', [])) if isinstance(ref_data.get('authors'), list) else ref_data.get('authors')
    
    cursor.execute("""
        INSERT OR REPLACE INTO paper_references 
        (citing_paper_id, cited_paper_id, title, authors, year, venue, abstract, citation_count, is_in_db)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        citing_paper_id,
        ref_data.get('cited_paper_id'),
        ref_data.get('title'),
        authors_json,
        ref_data.get('year'),
        ref_data.get('venue'),
        ref_data.get('abstract'),
        ref_data.get('citation_count', 0),
        ref_data.get('is_in_db', False)
    ))
    
    # Create cross-reference if cited paper is in DB
    if ref_data.get('cited_paper_id') and ref_data.get('is_in_db'):
        cursor.execute("""
            INSERT OR IGNORE INTO cross_references 
            (from_paper_id, to_paper_id, relationship_type, context)
            VALUES (?, ?, 'cites', ?)
        """, (
            citing_paper_id,
            ref_data['cited_paper_id'],
            f"Cited in {ref_data.get('title', 'references')}"
        ))

def insert_glossary_term(conn, term, definition, paper_id):
    """Insert or update a glossary term."""
    cursor = conn.cursor()
    
    # Check if term exists
    cursor.execute("SELECT occurrences FROM glossary WHERE term = ?", (term,))
    row = cursor.fetchone()
    
    if row:
        occurrences = json.loads(row['occurrences']) if row['occurrences'] else []
        if paper_id not in occurrences:
            occurrences.append(paper_id)
        cursor.execute("""
            UPDATE glossary 
            SET definition = ?, paper_id = ?, occurrences = ?
            WHERE term = ?
        """, (definition, paper_id, json.dumps(occurrences), term))
    else:
        cursor.execute("""
            INSERT INTO glossary (term, definition, paper_id, occurrences)
            VALUES (?, ?, ?, ?)
        """, (term, definition, paper_id, json.dumps([paper_id])))

def get_paper(conn, paper_id):
    """Get a paper by ID with all related data."""
    cursor = conn.cursor()
    
    # Get paper
    cursor.execute("SELECT * FROM papers WHERE paper_id = ?", (paper_id,))
    paper = dict(cursor.fetchone())
    
    # Parse JSON fields
    paper['authors'] = json.loads(paper['authors']) if paper['authors'] else []
    paper['tags'] = json.loads(paper['tags']) if paper['tags'] else []
    
    # Get figures
    cursor.execute("SELECT * FROM figures WHERE paper_id = ? ORDER BY figure_index", (paper_id,))
    paper['figures'] = [dict(row) for row in cursor.fetchall()]
    
    # Get references
    cursor.execute("SELECT * FROM paper_references WHERE citing_paper_id = ?", (paper_id,))
    paper['references'] = [dict(row) for row in cursor.fetchall()]
    
    # Get cited by (papers that cite this one)
    cursor.execute("""
        SELECT p.*, cr.context
        FROM cross_references cr
        JOIN papers p ON cr.from_paper_id = p.paper_id
        WHERE cr.to_paper_id = ? AND cr.relationship_type = 'cites'
    """, (paper_id,))
    paper['cited_by'] = [dict(row) for row in cursor.fetchall()]
    
    # Get related papers
    cursor.execute("""
        SELECT DISTINCT p.*, 'shared_reference' as relation_type
        FROM paper_references r1
        JOIN paper_references r2 ON r1.cited_paper_id = r2.cited_paper_id
        JOIN papers p ON r2.citing_paper_id = p.paper_id
        WHERE r1.citing_paper_id = ? AND p.paper_id != ?
        UNION
        SELECT DISTINCT p.*, cr.relationship_type as relation_type
        FROM cross_references cr
        JOIN papers p ON (cr.from_paper_id = p.paper_id OR cr.to_paper_id = p.paper_id)
        WHERE (cr.from_paper_id = ? OR cr.to_paper_id = ?) 
        AND p.paper_id != ?
        LIMIT 10
    """, (paper_id, paper_id, paper_id, paper_id, paper_id))
    paper['related'] = [dict(row) for row in cursor.fetchall()]
    
    # Get tags
    cursor.execute("""
        SELECT t.tag, t.description, t.color
        FROM tags t
        JOIN paper_tags pt ON t.tag = pt.tag
        WHERE pt.paper_id = ?
    """, (paper_id,))
    paper['tag_details'] = [dict(row) for row in cursor.fetchall()]
    
    return paper

def get_all_papers(conn):
    """Get all papers with basic info."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT paper_id, title, authors, year, venue, citation_count, tags, created_at
        FROM papers
        ORDER BY citation_count DESC, year DESC
    """)
    
    papers = []
    for row in cursor.fetchall():
        paper = dict(row)
        paper['authors'] = json.loads(paper['authors']) if paper['authors'] else []
        paper['tags'] = json.loads(paper['tags']) if paper['tags'] else []
        papers.append(paper)
    
    return papers

def get_glossary(conn):
    """Get all glossary terms."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM glossary ORDER BY term")
    return [dict(row) for row in cursor.fetchall()]

def search_papers(conn, query):
    """Search papers by title, abstract, or authors."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT paper_id, title, authors, year, venue, citation_count, abstract
        FROM papers
        WHERE title LIKE ? OR abstract LIKE ?
        ORDER BY citation_count DESC
    """, (f'%{query}%', f'%{query}%'))
    
    papers = []
    for row in cursor.fetchall():
        paper = dict(row)
        paper['authors'] = json.loads(paper['authors']) if paper['authors'] else []
        papers.append(paper)
    
    return papers

if __name__ == "__main__":
    init_db()
    print("Database schema created successfully!")
