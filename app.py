"""
ClawMart — MCP Server Registry & Discovery Platform
Agent-first. API-first. Built by Engine Room AI.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import time
import json
import traceback
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clawmart-secret-change-in-production')

from database import (
    init_db, get_all_servers, search_servers, get_server_by_id,
    get_server_count, get_categories_with_counts, save_submission,
    get_pending_submissions, approve_submission, reject_submission,
    log_api_usage, get_stats, get_api_stats
)
from seed_data import seed_if_empty

# Initialize
init_db()
seed_if_empty()

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'clawmart2024')


# ============================================
# AUTH (admin only)
# ============================================

def admin_required(f):
    """Decorator for admin-only routes."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        error = 'Wrong password'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))


# ============================================
# PUBLIC API (no auth — agent-facing)
# ============================================

@app.route('/api/v1/servers', methods=['GET'])
def api_list_servers():
    """List/search MCP servers. The core agent-facing endpoint."""
    start = time.time()

    query = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    tags = request.args.get('tags', '').strip()
    limit = min(int(request.args.get('limit', 50)), 200)

    if query or category or tags:
        servers = search_servers(query=query or None, category=category or None,
                                tags=tags or None, limit=limit)
    else:
        servers = get_all_servers(limit=limit)

    # Parse capabilities JSON for each server
    for s in servers:
        if isinstance(s.get('capabilities'), str):
            try:
                s['capabilities'] = json.loads(s['capabilities'])
            except (json.JSONDecodeError, TypeError):
                s['capabilities'] = {}

    elapsed = (time.time() - start) * 1000
    log_api_usage('/api/v1/servers', query_text=query or None,
                  user_agent=request.headers.get('User-Agent', '')[:200],
                  response_time_ms=elapsed)

    return jsonify({
        'status': 'success',
        'data': {
            'servers': servers,
            'total': len(servers),
            'limit': limit,
        },
        'metadata': {
            'api_version': 'v1',
            'response_time_ms': round(elapsed, 1)
        }
    })


@app.route('/api/v1/servers/<int:server_id>', methods=['GET'])
def api_get_server(server_id):
    """Get a single MCP server by ID."""
    start = time.time()
    server = get_server_by_id(server_id)

    if not server:
        return jsonify({'status': 'error', 'message': 'Server not found'}), 404

    if isinstance(server.get('capabilities'), str):
        try:
            server['capabilities'] = json.loads(server['capabilities'])
        except (json.JSONDecodeError, TypeError):
            server['capabilities'] = {}

    elapsed = (time.time() - start) * 1000
    log_api_usage(f'/api/v1/servers/{server_id}', server_id=server_id,
                  user_agent=request.headers.get('User-Agent', '')[:200],
                  response_time_ms=elapsed)

    return jsonify({
        'status': 'success',
        'data': server,
        'metadata': {
            'api_version': 'v1',
            'response_time_ms': round(elapsed, 1)
        }
    })


@app.route('/api/v1/discover', methods=['POST'])
def api_discover():
    """Claude-powered natural language discovery. The killer feature."""
    start = time.time()

    data = request.get_json(silent=True) or {}
    capability = data.get('capability', '').strip()

    if not capability or len(capability) < 5:
        return jsonify({
            'status': 'error',
            'message': 'Please provide a capability description (minimum 5 characters)',
            'example': {'capability': 'I need to read and write files on the local system'}
        }), 400

    limit = min(int(data.get('limit', 5)), 10)

    try:
        from discovery import discover_servers
        matches = discover_servers(capability, limit=limit)

        # Parse capabilities JSON in matched servers
        for m in matches:
            s = m.get('server', {})
            if isinstance(s.get('capabilities'), str):
                try:
                    s['capabilities'] = json.loads(s['capabilities'])
                except (json.JSONDecodeError, TypeError):
                    s['capabilities'] = {}

        elapsed = (time.time() - start) * 1000
        log_api_usage('/api/v1/discover', query_text=capability,
                      user_agent=request.headers.get('User-Agent', '')[:200],
                      response_time_ms=elapsed)

        return jsonify({
            'status': 'success',
            'data': {
                'query': capability,
                'matches': matches,
                'count': len(matches),
            },
            'metadata': {
                'api_version': 'v1',
                'response_time_ms': round(elapsed, 1),
                'powered_by': 'Claude (Anthropic)'
            }
        })
    except Exception as e:
        print(f"[API] Discover error: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/v1/categories', methods=['GET'])
def api_categories():
    """List all categories with server counts."""
    cats = get_categories_with_counts()
    return jsonify({
        'status': 'success',
        'data': [{'name': name, 'count': count} for name, count in cats]
    })


# ============================================
# WEB UI (human-facing)
# ============================================

@app.route('/')
def home():
    stats = get_stats()
    api_stats = get_api_stats()
    return render_template('home.html', stats=stats, api_stats=api_stats)


@app.route('/browse')
def browse():
    query = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    if query or category:
        servers = search_servers(query=query or None, category=category or None, limit=100)
    else:
        servers = get_all_servers(limit=100)

    # Parse capabilities
    for s in servers:
        if isinstance(s.get('capabilities'), str):
            try:
                s['capabilities'] = json.loads(s['capabilities'])
            except (json.JSONDecodeError, TypeError):
                s['capabilities'] = {}

    categories = get_categories_with_counts()
    return render_template('browse.html', servers=servers, categories=categories,
                           query=query, current_category=category)


@app.route('/servers/<int:server_id>')
def server_detail(server_id):
    server = get_server_by_id(server_id)
    if not server:
        return "Server not found", 404

    if isinstance(server.get('capabilities'), str):
        try:
            server['capabilities'] = json.loads(server['capabilities'])
        except (json.JSONDecodeError, TypeError):
            server['capabilities'] = {}

    return render_template('server_detail.html', server=server)


@app.route('/submit', methods=['GET', 'POST'])
def submit_server():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'description': request.form.get('description', '').strip(),
            'version': request.form.get('version', '').strip(),
            'author': request.form.get('author', '').strip(),
            'repo_url': request.form.get('repo_url', '').strip(),
            'install_command': request.form.get('install_command', '').strip(),
            'transport_type': request.form.get('transport_type', 'stdio'),
            'categories': request.form.get('categories', '').strip(),
            'tags': request.form.get('tags', '').strip(),
            'capabilities': request.form.get('capabilities', '{}').strip(),
        }

        if not data['name']:
            return render_template('submit.html', error='Server name is required', data=data)

        save_submission(data)
        return render_template('submit.html', success=True, data={})

    return render_template('submit.html', data={})


@app.route('/docs')
def api_docs():
    return render_template('api_docs.html')


# ============================================
# ADMIN
# ============================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = get_stats()
    pending = get_pending_submissions()
    api_stats = get_api_stats()
    return render_template('admin.html', stats=stats, pending=pending, api_stats=api_stats)


@app.route('/admin/approve/<int:sub_id>', methods=['POST'])
@admin_required
def admin_approve(sub_id):
    approve_submission(sub_id)
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/reject/<int:sub_id>', methods=['POST'])
@admin_required
def admin_reject(sub_id):
    reason = request.form.get('reason', '')
    reject_submission(sub_id, reason)
    return redirect(url_for('admin_dashboard'))


# ============================================
# HEALTH CHECK
# ============================================

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'clawmart',
        'version': '1.0',
        'servers_count': get_server_count()
    })


if __name__ == '__main__':
    app.run(debug=True, port=5003)
