import sys
import os
import json
from pathlib import Path
from parse_coppermind_wiki import parse_world, parse_book, parse_character

# Usage: python3 bulk_parse_coppermind_wiki.py <input_dir>
if len(sys.argv) < 2:
    print("Usage: python3 bulk_parse_coppermind_wiki.py <input_dir>")
    sys.exit(1)

input_dir = Path(sys.argv[1])
output_dir = Path("backend/data")
output_dir.mkdir(parents=True, exist_ok=True)

worlds = []
books = []
characters = []

for file in input_dir.glob("*.html"):
    with open(file, 'r', encoding='utf-8') as f:
        first_1k = f.read(1024).lower()
    # Heuristic: classify by infobox/template
    if '{{shardworld' in first_1k:
        worlds.append(parse_world(str(file)))
    elif '{{book' in first_1k:
        books.append(parse_book(str(file)))
    elif '{{character' in first_1k or '{{infobox character' in first_1k:
        characters.append(parse_character(str(file)))
    else:
        print(f"[WARN] Could not classify: {file}")

with open(output_dir / "worlds.json", "w") as f:
    json.dump(worlds, f, indent=2)
with open(output_dir / "books.json", "w") as f:
    json.dump(books, f, indent=2)
with open(output_dir / "characters.json", "w") as f:
    json.dump(characters, f, indent=2)

print(f"✅ Bulk parsed {len(worlds)} worlds, {len(books)} books, {len(characters)} characters from {input_dir}") 