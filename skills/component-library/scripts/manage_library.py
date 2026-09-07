#!/usr/bin/env python3
"""
Manage index.json for the component-library skill.

This script is the only thing that should write to library/index.json.
It keeps metadata well-formed and prevents duplicate/mismatched IDs.
The actual component file (self-contained HTML/CSS/JS) is written/edited
directly with normal file tools (Read/Write/Edit) -- this script only
tracks metadata about it.

Usage:
  python manage_library.py add --name NAME --category CAT \
      --file RELATIVE/PATH.html --description "..." \
      [--tags a,b,c] [--source prompt|image|code]
  python manage_library.py list [--category CAT] [--tag TAG] [--query TEXT]
  python manage_library.py get --name NAME
  python manage_library.py update --name NAME [--description "..."] \
      [--category CAT] [--tags a,b,c] [--rename NEW_NAME]
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

VALID_SOURCES = {"prompt", "image", "code"}


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
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return slug


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
        print(f"Error: a component named '{args.name}' already exists (id: {slug}). "
              f"Use 'update' instead, or pick a different name.", file=sys.stderr)
        sys.exit(1)

    source = args.source or "prompt"
    if source not in VALID_SOURCES:
        print(f"Error: --source must be one of {sorted(VALID_SOURCES)}", file=sys.stderr)
        sys.exit(1)

    code_path = LIBRARY_DIR / args.file
    if not code_path.exists():
        print(f"Warning: {code_path} does not exist yet. "
              f"Write the component file there before (or right after) registering it.",
              file=sys.stderr)

    entry = {
        "id": slug,
        "name": args.name.strip(),
        "category": args.category.strip(),
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
        "source": source,
        "description": args.description.strip(),
        "file": args.file,
    }
    entries.append(entry)
    save_index(entries)
    print(f"Added '{entry['name']}' (id: {slug}) to the library.")


def cmd_list(args):
    entries = load_index()

    if args.category:
        entries = [e for e in entries if e["category"].lower() == args.category.lower()]
    if args.tag:
        entries = [e for e in entries if args.tag.lower() in [t.lower() for t in e.get("tags", [])]]
    if args.query:
        q = args.query.lower()
        entries = [
            e for e in entries
            if q in e["name"].lower()
            or q in e.get("description", "").lower()
            or q in e["category"].lower()
            or any(q in t.lower() for t in e.get("tags", []))
        ]

    if not entries:
        print("No matching components found.")
        return

    for e in entries:
        tags = ", ".join(e.get("tags", []))
        print(f"- {e['name']}  [{e['category']}]  (source: {e.get('source', 'prompt')})")
        print(f"    tags: {tags or '(none)'}")
        print(f"    {e.get('description', '')}")
        print(f"    file: library/{e['file']}")


def cmd_get(args):
    entries = load_index()
    entry = find_entry(entries, args.name)
    if not entry:
        print(f"Error: no component named '{args.name}' found.", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(entry, indent=2, ensure_ascii=False))
    code_path = LIBRARY_DIR / entry["file"]
    if code_path.exists():
        print("\n--- code ---")
        print(code_path.read_text(encoding="utf-8"))
    else:
        print(f"\n(warning: code file {code_path} is missing)", file=sys.stderr)


def cmd_update(args):
    entries = load_index()
    entry = find_entry(entries, args.name)
    if not entry:
        print(f"Error: no component named '{args.name}' found.", file=sys.stderr)
        sys.exit(1)

    if args.description is not None:
        entry["description"] = args.description
    if args.category is not None:
        entry["category"] = args.category
    if args.tags is not None:
        entry["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    if args.rename is not None:
        entry["name"] = args.rename
        entry["id"] = slugify(args.rename)

    save_index(entries)
    print(f"Updated '{entry['name']}'.")


def cmd_remove(args):
    entries = load_index()
    entry = find_entry(entries, args.name)
    if not entry:
        print(f"Error: no component named '{args.name}' found.", file=sys.stderr)
        sys.exit(1)

    code_path = LIBRARY_DIR / entry["file"]
    if code_path.exists():
        code_path.unlink()

    entries = [e for e in entries if e["id"] != entry["id"]]
    save_index(entries)
    print(f"Removed '{entry['name']}' from the library.")


def main():
    parser = argparse.ArgumentParser(description="Manage the component library's index.json")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Register a new component")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--category", required=True)
    p_add.add_argument("--file", required=True, help="Path relative to library/")
    p_add.add_argument("--description", required=True)
    p_add.add_argument("--tags", default="")
    p_add.add_argument("--source", default="prompt", help="prompt|image|code")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List components, optionally filtered")
    p_list.add_argument("--category")
    p_list.add_argument("--tag")
    p_list.add_argument("--query")
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Show full metadata + code for one component")
    p_get.add_argument("--name", required=True)
    p_get.set_defaults(func=cmd_get)

    p_update = sub.add_parser("update", help="Update metadata fields for a component")
    p_update.add_argument("--name", required=True)
    p_update.add_argument("--description")
    p_update.add_argument("--category")
    p_update.add_argument("--tags")
    p_update.add_argument("--rename")
    p_update.set_defaults(func=cmd_update)

    p_remove = sub.add_parser("remove", help="Remove a component and its file")
    p_remove.add_argument("--name", required=True)
    p_remove.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
