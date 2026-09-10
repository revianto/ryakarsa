#!/bin/bash
# API Tester login — run this yourself in your own terminal (not via Claude's
# Bash tool) so your password is typed directly and never appears in chat/context.
set -euo pipefail

BASE_URL="https://apitester.staging.indociti.com"
TOKEN_DIR="$HOME/.config/apitester-skill"
TOKEN_FILE="$TOKEN_DIR/token.json"

mkdir -p "$TOKEN_DIR"
chmod 700 "$TOKEN_DIR"

echo "API Tester email: "
read -r AT_EMAIL

echo "API Tester password (hidden): "
read -rs AT_PASSWORD
echo

RESPONSE=$(curl -s -X POST "${BASE_URL}/api/v1/auth/login" \
  -H 'content-type: application/json' \
  --data-raw "$(python3 -c "import json,sys; print(json.dumps({'email': sys.argv[1], 'password': sys.argv[2]}))" "$AT_EMAIL" "$AT_PASSWORD")")

ACCESS_TOKEN=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('access_token',''))" 2>/dev/null || true)

if [ -z "$ACCESS_TOKEN" ]; then
  echo ""
  echo "LOGIN GAGAL. Response dari server:"
  echo "$RESPONSE"
  exit 1
fi

echo "$RESPONSE" > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"

echo ""
echo "Login berhasil. Token tersimpan di ${TOKEN_FILE}"
echo "Sekarang beri tahu Claude untuk melanjutkan (mis. 'lanjut, sudah login')."
