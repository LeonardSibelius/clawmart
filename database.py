"""
ClawMart — Database layer (SQLite)
MCP Server Registry & Discovery Platform
"""

import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'clawmart.db')


def get_db():
    """Get database connection with row factory."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            icon TEXT
        );

        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            version TEXT,
            author TEXT,
            repo_url TEXT,
            install_command TEXT,
            transport_type TEXT DEFAULT 'stdio',
            categories TEXT,
            capabilities TEXT,
            tags TEXT,
            popularity_score REAL DEFAULT 0,
            status TEXT DEFAULT 'approved',
            created_at TEXT,
            updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            version TEXT,
            author TEXT,
            repo_url TEXT,
            install_command TEXT,
            transport_type TEXT DEFAULT 'stdio',
            categories TEXT,
            capabilities TEXT,
            tags TEXT,
            submitted_at TEXT,
            status TEXT DEFAULT 'pending',
            rejection_reason TEXT
        );

        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            query_text TEXT,
            server_id INTEGER,
            user_agent TEXT,
            timestamp TEXT,
            response_time_ms REAL,
            FOREIGN KEY (server_id) REFERENCES servers(id)
        );

        CREATE INDEX IF NOT EXISTS idx_servers_status ON servers(status);
        CREATE INDEX IF NOT EXISTS idx_servers_categories ON servers(categories);
        CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);
        CREATE INDEX IF NOT EXISTS idx_api_usage_timestamp ON api_usage(timestamp);
    """)
    conn.commit()
    conn.close()


# ============================================
# SERVERS
# ============================================

def add_server(data):
    """Insert a server into the registry."""
    conn = get_db()
    now = datetime.utcnow().isoformat()
    capabilities = data.get('capabilities', '{}')
    if isinstance(capabilities, dict):
        capabilities = json.dumps(capabilities)

    conn.execute("""
        INSERT INTO servers (name, description, version, author, repo_url,
            install_command, transport_type, categories, capabilities, tags,
            status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'approved', ?, ?)
    """, (
        data['name'], data.get('description', ''), data.get('version', ''),
        data.get('author', ''), data.get('repo_url', ''),
        data.get('install_command', ''), data.get('transport_type', 'stdio'),
        data.get('categories', ''), capabilities,
        data.get('tags', ''), now, now
    ))
    conn.commit()
    conn.close()


def get_all_servers(limit=100):
    """Get all approved servers."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM servers WHERE status='approved' ORDER BY popularity_score DESC, name ASC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_servers(query=None, category=None, tags=None, limit=50):
    """Search servers by text, category, or tags."""
    conn = get_db()
    sql = "SELECT * FROM servers WHERE status='approved'"
    params = []

    if query:
        sql += " AND (name LIKE ? OR description LIKE ? OR tags LIKE ?)"
        q = f"%{query}%"
        params.extend([q, q, q])

    if category:
        sql += " AND categories LIKE ?"
        params.append(f"%{category}%")

    if tags:
        for tag in tags.split(','):
            sql += " AND tags LIKE ?"
            params.append(f"%{tag.strip()}%")

    sql += " ORDER BY popularity_score DESC, name ASC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_server_by_id(server_id):
    """Get a single server by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM servers WHERE id=?", (server_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_server_count():
    """Count approved servers."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM servers WHERE status='approved'").fetchone()[0]
    conn.close()
    return count


def get_categories_with_counts():
    """Get all categories with server counts."""
    servers = get_all_servers(limit=1000)
    cat_counts = {}
    for s in servers:
        for cat in (s.get('categories') or '').split(','):
            cat = cat.strip()
            if cat:
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
    return sorted(cat_counts.items(), key=lambda x: -x[1])


# ============================================
# SUBMISSIONS
# ============================================

def save_submission(data):
    """Save a new server submission for review."""
    conn = get_db()
    now = datetime.utcnow().isoformat()
    capabilities = data.get('capabilities', '{}')
    if isinstance(capabilities, dict):
        capabilities = json.dumps(capabilities)

    conn.execute("""
        INSERT INTO submissions (name, description, version, author, repo_url,
            install_command, transport_type, categories, capabilities, tags,
            submitted_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (
        data['name'], data.get('description', ''), data.get('version', ''),
        data.get('author', ''), data.get('repo_url', ''),
        data.get('install_command', ''), data.get('transport_type', 'stdio'),
        data.get('categories', ''), capabilities,
        data.get('tags', ''), now
    ))
    conn.commit()
    conn.close()


def get_pending_submissions():
    """Get all pending submissions."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM submissions WHERE status='pending' ORDER BY submitted_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def approve_submission(submission_id):
    """Approve a submission — move to servers table."""
    conn = get_db()
    sub = conn.execute("SELECT * FROM submissions WHERE id=?", (submission_id,)).fetchone()
    if not sub:
        conn.close()
        return False

    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO servers (name, description, version, author, repo_url,
            install_command, transport_type, categories, capabilities, tags,
            status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'approved', ?, ?)
    """, (
        sub['name'], sub['description'], sub['version'], sub['author'],
        sub['repo_url'], sub['install_command'], sub['transport_type'],
        sub['categories'], sub['capabilities'], sub['tags'], now, now
    ))
    conn.execute("UPDATE submissions SET status='approved' WHERE id=?", (submission_id,))
    conn.commit()
    conn.close()
    return True


def reject_submission(submission_id, reason=''):
    """Reject a submission."""
    conn = get_db()
    conn.execute(
        "UPDATE submissions SET status='rejected', rejection_reason=? WHERE id=?",
        (reason, submission_id)
    )
    conn.commit()
    conn.close()


# ============================================
# ANALYTICS
# ============================================

def log_api_usage(endpoint, query_text=None, server_id=None, user_agent='', response_time_ms=0):
    """Log an API call for analytics."""
    conn = get_db()
    conn.execute("""
        INSERT INTO api_usage (endpoint, query_text, server_id, user_agent, timestamp, response_time_ms)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (endpoint, query_text, server_id, (user_agent or '')[:200],
          datetime.utcnow().isoformat(), response_time_ms))
    conn.commit()
    conn.close()


def get_api_stats():
    """Get API usage statistics."""
    conn = get_db()
    total_calls = conn.execute("SELECT COUNT(*) FROM api_usage").fetchone()[0]
    discover_calls = conn.execute(
        "SELECT COUNT(*) FROM api_usage WHERE endpoint='/api/v1/discover'"
    ).fetchone()[0]
    conn.close()
    return {'total_api_calls': total_calls, 'discover_calls': discover_calls}


def get_stats():
    """Get overall stats for dashboard."""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM servers WHERE status='approved'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM submissions WHERE status='pending'").fetchone()[0]
    api_calls = conn.execute("SELECT COUNT(*) FROM api_usage").fetchone()[0]
    conn.close()
    return {'total_servers': total, 'pending_submissions': pending, 'api_calls': api_calls}
