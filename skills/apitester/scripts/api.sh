#!/bin/bash
# Olsera API Tester helper — safe for Claude to run (no credentials touched
# here, only the already-established access/refresh token file).
#
# Usage:
#   api.sh GET    "/api/v1/collections"
#   api.sh GET    "/api/v1/collections/<id>"
#   api.sh POST   "/api/v1/collections/<id>/requests" '{"name":"...","method":"GET","url":"..."}'
#   api.sh PUT    "/api/v1/requests/<id>" '{"name":"...","method":"GET","url":"..."}'
#   api.sh DELETE "/api/v1/requests/<id>"
set -euo pipefail

BASE_URL="https://apitester.staging.indociti.com"
TOKEN_FILE="$HOME/.config/apitester-skill/token.json"

METHOD="${1:-}"
PATH_PART="${2:-}"
BODY="${3:-}"

if [ -z "$METHOD" ] || [ -z "$PATH_PART" ]; then
  echo "Usage: api.sh <GET|POST|PUT|DELETE> <path> [json-body]" >&2
  exit 2
fi

if [ ! -f "$TOKEN_FILE" ]; then
  echo '{"error":"NOT_LOGGED_IN","message":"Belum login. Minta user menjalankan ~/.agents/skills/apitester/scripts/login.sh di terminal mereka sendiri."}' >&2
  exit 1
fi

ACCESS_TOKEN=$(python3 -c "import json; print(json.load(open('$TOKEN_FILE')).get('access_token',''))")

call_api() {
  local token="$1"
  ARGS=(-s -w "\n__HTTP_STATUS__:%{http_code}" --url "${BASE_URL}${PATH_PART}" \
    -H 'accept: */*' -H "authorization: Bearer ${token}")
  if [ -n "$BODY" ]; then
    ARGS+=(-H 'content-type: application/json' -X "$METHOD" --data-raw "$BODY")
  else
    ARGS+=(-X "$METHOD")
  fi
  curl "${ARGS[@]}"
}

RAW=$(call_api "$ACCESS_TOKEN")
STATUS=$(echo "$RAW" | grep -o '__HTTP_STATUS__:[0-9]*' | cut -d: -f2)
BODY_OUT=$(echo "$RAW" | sed 's/__HTTP_STATUS__:[0-9]*$//')

if [ "$STATUS" = "401" ]; then
  echo '{"error":"SESSION_EXPIRED","message":"Sesi API Tester sudah kedaluwarsa. Minta user menjalankan ~/.agents/skills/apitester/scripts/login.sh lagi di terminal mereka sendiri."}' >&2
  exit 1
fi

echo "$BODY_OUT"

if [ "$STATUS" -ge 400 ]; then
  exit 1
fi
