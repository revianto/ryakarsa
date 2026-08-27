#!/usr/bin/env bash
# Sinkronisasi skill dari ~/.agents/skills ke repo ini, lalu commit & push jika ada perubahan.
# Sumber kebenaran: ~/.agents/skills/<skill>. Salinan di repo ikut persis (rsync --delete).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$HOME/.agents/skills"
SKILLS=(prd prd-refine)

for s in "${SKILLS[@]}"; do
  if [ ! -d "$SRC/$s" ]; then
    echo "LEWATI: $s tidak ada di $SRC"
    continue
  fi
  rsync -a --delete "$SRC/$s/" "$REPO/skills/$s/"
done

cd "$REPO"

if git diff --quiet && [ -z "$(git status --porcelain)" ]; then
  echo "TIDAK ADA PERUBAHAN"
  exit 0
fi

# Validasi: frontmatter wajib benar sebelum boleh push
for f in skills/*/SKILL.md; do
  dir="$(basename "$(dirname "$f")")"
  grep -q "^name: $dir$" "$f" || { echo "VALIDASI GAGAL: $f — 'name' harus '$dir'"; exit 1; }
  grep -q "^description:" "$f" || { echo "VALIDASI GAGAL: $f — 'description' wajib ada"; exit 1; }
done

git add -A
git commit -m "chore: sinkronisasi skill dari ~/.agents/skills"
git push origin main
echo "TERPUSH: $(git rev-parse --short HEAD)"
