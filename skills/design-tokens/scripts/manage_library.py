#!/usr/bin/env python3
"""
Manage index.json for the design-tokens skill.

This script is the only thing that should write to library/index.json.
It keeps metadata well-formed and prevents duplicate/mismatched IDs.

Each entry represents one whole DESIGN SYSTEM. Its actual token values
(color, typography, spacing, radius, shadow, breakpoint, motion, z-index --
all nested together) live in one JSON file at library/<id>/tokens.json,
written/edited directly with normal file tools (Read/Write/Edit) -- this
script only tracks metadata about it (name, description, tags, source).

Usage:
  python manage_library.py add --name NAME \
      [--description "..."] [--tags a,b,c] [--source design|prompt|code]
      (creates library/<id>/tokens.json with an empty category skeleton
       if it does not already exist)
  python manage_library.py list [--tag TAG] [--query TEXT]
  python manage_library.py get --name NAME
  python manage_library.py update --name NAME [--description "..."] \
      [--tags a,b,c] [--rename NEW_NAME]
  python manage_library.py remove --name NAME
"""

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
LIBRARY_DIR = SKILL_DIR / "library"
INDEX_PATH = LIBRARY_DIR / "index.json"

VALID_SOURCES = {"design", "prompt", "code"}

EMPTY_TOKEN_SKELETON = {
    "color": {"primitive": {}, "semantic": {}},
    "typography": {"fontFamily": {}, "scale": {}, "weight": {}, "lineHeight": {}},
    "spacing": {},
    "radius": {},
    "shadow": {},
    "breakpoint": {},
    "motion": {"duration": {}, "easing": {}},
    "z-index": {},
}


def load_index():
    if not INDEX_PATH.exists():
        return []
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_index(entries):
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")


def find_entry(entries, name):
    slug = slugify(name)
    for e in entries:
        if e["id"] == slug or e["name"].lower() == name.strip().lower():
            return e
    return None


def cmd_add(args):
    entries = load_index()
    slug = slugify(args.name)

    if find_entry(entries, args.name):
        print(f"Error: a design system named '{args.name}' already exists (id: {slug}). "
              f"Use 'update' instead, or pick a different name.", file=sys.stderr)
        sys.exit(1)

    source = args.source or "design"
    if source not in VALID_SOURCES:
        print(f"Error: --source must be one of {sorted(VALID_SOURCES)}", file=sys.stderr)
        sys.exit(1)

    rel_file = f"{slug}/tokens.json"
    token_path = LIBRARY_DIR / rel_file
    if not token_path.exists():
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, "w", encoding="utf-8") as f:
            json.dump(EMPTY_TOKEN_SKELETON, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Created empty token skeleton at library/{rel_file} -- fill it in with Edit/Write.")

    entry = {
        "id": slug,
        "name": args.name.strip(),
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
        "source": source,
        "description": (args.description or "").strip(),
        "file": rel_file,
    }
    entries.append(entry)
    save_index(entries)
    print(f"Added design system '{entry['name']}' (id: {slug}) to the library.")


def cmd_list(args):
    entries = load_index()

    if args.tag:
        entries = [e for e in entries if args.tag.lower() in [t.lower() for t in e.get("tags", [])]]
    if args.query:
        q = args.query.lower()
        entries = [
            e for e in entries
            if q in e["name"].lower()
            or q in e.get("description", "").lower()
            or any(q in t.lower() for t in e.get("tags", []))
        ]

    if not entries:
        print("No matching design systems found.")
        return

    for e in entries:
        tags = ", ".join(e.get("tags", []))
        print(f"- {e['name']}  (source: {e.get('source', 'design')})")
        print(f"    tags: {tags or '(none)'}")
        print(f"    {e.get('description', '')}")
        print(f"    file: library/{e['file']}")


def cmd_get(args):
    entries = load_index()
    entry = find_entry(entries, args.name)
    if not entry:
        print(f"Error: no design system named '{args.name}' found.", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(entry, indent=2, ensure_ascii=False))
    token_path = LIBRARY_DIR / entry["file"]
    if token_path.exists():
        print("\n--- tokens ---")
        print(token_path.read_text(encoding="utf-8"))
    else:
        print(f"\n(warning: token file {token_path} is missing)", file=sys.stderr)


def cmd_update(args):
    entries = load_index()
    entry = find_entry(entries, args.name)
    if not entry:
        print(f"Error: no design system named '{args.name}' found.", file=sys.stderr)
        sys.exit(1)

    if args.description is not None:
        entry["description"] = args.description
    if args.tags is not None:
        entry["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    if args.rename is not None:
        old_dir = LIBRARY_DIR / entry["id"]
        new_slug = slugify(args.rename)
        new_dir = LIBRARY_DIR / new_slug
        if old_dir.exists() and old_dir != new_dir:
            old_dir.rename(new_dir)
            entry["file"] = f"{new_slug}/tokens.json"
        entry["name"] = args.rename
        entry["id"] = new_slug

    save_index(entries)
    print(f"Updated '{entry['name']}'.")


def cmd_remove(args):
    entries = load_index()
    entry = find_entry(entries, args.name)
    if not entry:
        print(f"Error: no design system named '{args.name}' found.", file=sys.stderr)
        sys.exit(1)

    sys_dir = LIBRARY_DIR / entry["id"]
    if sys_dir.exists():
        for f in sys_dir.iterdir():
            f.unlink()
        sys_dir.rmdir()

    entries = [e for e in entries if e["id"] != entry["id"]]
    save_index(entries)
    print(f"Removed design system '{entry['name']}' from the library.")


def main():
    parser = argparse.ArgumentParser(description="Manage the design-tokens library's index.json")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Register a new design system")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--description", default="")
    p_add.add_argument("--tags", default="")
    p_add.add_argument("--source", default="design", help="design|prompt|code")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List design systems, optionally filtered")
    p_list.add_argument("--tag")
    p_list.add_argument("--query")
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Show full metadata + tokens for one design system")
    p_get.add_argument("--name", required=True)
    p_get.set_defaults(func=cmd_get)

    p_update = sub.add_parser("update", help="Update metadata fields for a design system")
    p_update.add_argument("--name", required=True)
    p_update.add_argument("--description")
    p_update.add_argument("--tags")
    p_update.add_argument("--rename")
    p_update.set_defaults(func=cmd_update)

    p_remove = sub.add_parser("remove", help="Remove a design system and all its tokens")
    p_remove.add_argument("--name", required=True)
    p_remove.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
