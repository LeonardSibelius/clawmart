"""
ClawMart — Claude-Powered Discovery Engine
The killer feature: agents describe what they need, Claude finds the right MCP servers.
"""

import os
import json
import time
from anthropic import Anthropic
from database import get_all_servers

client = None


def get_client():
    global client
    if client is None:
        client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
    return client


def discover_servers(capability_description, limit=5):
    """
    Take a natural language capability description and match it to MCP servers.

    Args:
        capability_description: What the agent needs, e.g. "I need to read and write files"
        limit: Max number of matches to return

    Returns:
        List of matched servers with reasons
    """
    servers = get_all_servers(limit=200)
    if not servers:
        return []

    # Build a compact server catalog for Claude
    catalog = []
    for s in servers:
        caps = s.get('capabilities', '{}')
        if isinstance(caps, str):
            try:
                caps = json.loads(caps)
            except json.JSONDecodeError:
                caps = {}

        catalog.append({
            'id': s['id'],
            'name': s['name'],
            'description': s['description'],
            'categories': s.get('categories', ''),
            'tags': s.get('tags', ''),
            'tools': caps.get('tools', []),
            'resources': caps.get('resources', []),
        })

    catalog_json = json.dumps(catalog, indent=1)

    prompt = f"""You are ClawMart's discovery engine. An AI agent is looking for MCP servers that match their needs.

AGENT'S REQUEST:
"{capability_description}"

AVAILABLE MCP SERVERS:
{catalog_json}

YOUR TASK:
Find the {limit} most relevant MCP servers for this request. Consider:
- Tool names and what they do
- Server descriptions
- Tags and categories
- Whether the server actually solves the agent's need

Return ONLY valid JSON (no markdown, no explanation outside the JSON):
{{
  "matches": [
    {{
      "id": <server_id>,
      "relevance_score": <1-10>,
      "reason": "<one sentence explaining why this server matches>"
    }}
  ]
}}

If nothing matches well, return {{"matches": []}}. Only include servers with relevance >= 6."""

    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text.strip()
        # Strip markdown code fences if present
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()

        result = json.loads(text)
        matches = result.get('matches', [])

        # Enrich matches with full server data
        server_map = {s['id']: s for s in servers}
        enriched = []
        for m in matches[:limit]:
            server = server_map.get(m['id'])
            if server:
                enriched.append({
                    'server': server,
                    'relevance_score': m.get('relevance_score', 0),
                    'reason': m.get('reason', '')
                })

        return enriched

    except json.JSONDecodeError as e:
        print(f"[Discovery] JSON parse error: {e}")
        print(f"[Discovery] Raw response: {text[:500]}")
        return []
    except Exception as e:
        print(f"[Discovery] Error: {e}")
        return []
