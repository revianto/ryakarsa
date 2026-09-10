#!/bin/bash
# Resolve a collection's id from a partial name match.
# Usage: resolve_collection.sh "<partial collection name>"
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
QUERY="${1:-}"

if [ -z "$QUERY" ]; then
  echo "Usage: resolve_collection.sh \"<partial collection name>\"" >&2
  exit 2
fi

"$SCRIPT_DIR/api.sh" GET "/api/v1/collections" | python3 -c "
import json, sys
query = sys.argv[1].lower()
data = json.load(sys.stdin)
matches = [
    {'id': c['id'], 'name': c['name'], 'permission': c.get('permission')}
    for c in data.get('data', [])
    if query in c['name'].lower()
]
print(json.dumps(matches, indent=2))
" "$QUERY"
