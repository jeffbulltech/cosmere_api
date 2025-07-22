import sys
import os
import json
import re
from pathlib import Path
from parse_coppermind_wiki import parse_world, parse_book, parse_character

def parse_shard(file_path: str) -> dict:
    # Placeholder: parse as book for now, or implement real logic
    return parse_book(file_path)

def parse_magic_system(file_path: str) -> dict:
    # Placeholder: parse as book for now, or implement real logic
    return parse_book(file_path)

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
shards = []
magic_systems = []

for file in input_dir.glob("*.html"):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read(2048).lower()  # Read more for safety
    # Regex: find the first {{template_name
    m = re.search(r'\{\{\s*([a-z0-9_ ]+)', content)
    infobox = m.group(1).strip() if m else None
    if infobox:
        if 'shardworld' in infobox:
            worlds.append(parse_world(str(file)))
        elif 'character' in infobox:
            characters.append(parse_character(str(file)))
        elif 'book' in infobox:
            books.append(parse_book(str(file)))
        elif 'shard info' in infobox:
            shards.append(parse_shard(str(file)))
        elif 'magic' in infobox:
            magic_systems.append(parse_magic_system(str(file)))
        else:
            print(f"[WARN] Unrecognized infobox '{infobox}' in {file}")
    else:
        print(f"[WARN] No infobox found in {file}")

with open(output_dir / "worlds.json", "w") as f:
    json.dump(worlds, f, indent=2)
with open(output_dir / "books.json", "w") as f:
    json.dump(books, f, indent=2)
with open(output_dir / "characters.json", "w") as f:
    json.dump(characters, f, indent=2)
with open(output_dir / "shards.json", "w") as f:
    json.dump(shards, f, indent=2)
with open(output_dir / "magic_systems.json", "w") as f:
    json.dump(magic_systems, f, indent=2)

print(f"✅ Bulk parsed {len(worlds)} worlds, {len(books)} books, {len(characters)} characters, {len(shards)} shards, {len(magic_systems)} magic systems from {input_dir}") 