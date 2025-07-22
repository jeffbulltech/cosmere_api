import re
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Utility functions

def clean_wikilinks(text: str) -> str:
    # Remove [[...]] and keep the display text or link name
    return re.sub(r'\[\[(?:[^\]]|\n)*?\]\]', lambda m: m.group(0)[2:-2].split('|')[-1], text)

def clean_html(text: str) -> str:
    # Remove <br />, <small>, etc.
    text = re.sub(r'<br\s*/?>', ', ', text)
    text = re.sub(r'<.*?>', '', text)
    return text

def clean_refs(text: str) -> str:
    # Remove {{book ref|...}}, {{au ref|...}}, etc.
    return re.sub(r'\{\{[^}]+\}\}', '', text)

def clean_value(text: str) -> str:
    return clean_refs(clean_html(clean_wikilinks(text))).strip(' ,\n')

def parse_infobox(lines, start_idx) -> (Dict[str, str], int):
    data = {}
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('}}'):
            break
        if line.startswith('|'):
            if '=' in line:
                key, value = line[1:].split('=', 1)
                data[key.strip().lower()] = clean_value(value.strip())
        i += 1
    return data, i

def extract_narrative(lines, start_idx) -> str:
    # Join the rest of the lines, skipping templates and quotes
    narrative = []
    in_template = False
    for line in lines[start_idx:]:
        if line.strip().startswith('{{'):
            in_template = True
        if in_template and line.strip().endswith('}}'):
            in_template = False
            continue
        if not in_template and not line.strip().startswith("'''"):
            narrative.append(line)
    return clean_refs(clean_html(' '.join(narrative))).strip()

def parse_world(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Find infobox
    for i, line in enumerate(lines):
        if line.strip().startswith('{{Shardworld'):
            infobox, end_idx = parse_infobox(lines, i+1)
            break
    else:
        infobox, end_idx = {"name": Path(file_path).stem}, 0
    # Narrative
    narrative = extract_narrative(lines, end_idx+1)
    # Build world dict
    world = {
        "id": infobox.get("name", Path(file_path).stem).lower().replace(' ', '_'),
        "name": infobox.get("name", Path(file_path).stem),
        "system": infobox.get("system"),
        "geography": {
            "gravity": infobox.get("gravity"),
            "radius": infobox.get("radius"),
            "map": infobox.get("map"),
        },
        "magic_systems": [m.strip() for m in infobox.get("magic", "").split(',') if m.strip()],
        "shards": [s.strip() for s in infobox.get("shards", "").split(',') if s.strip()],
        "perpendicularities": [p.strip() for p in infobox.get("perpendicularity", "").split(',') if p.strip()],
        "books": [b.strip() for b in infobox.get("books", "").split(',') if b.strip()],
        "description": narrative[:1000]  # Truncate for brevity
    }
    return world

def parse_book(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Find infobox (case-insensitive)
    infobox = None
    end_idx = 0
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('{{book'):
            infobox, end_idx = parse_infobox(lines, i+1)
            break
    if not infobox:
        infobox, end_idx = {"title": Path(file_path).stem}, 0
    # Lowercase all infobox keys for easier access
    infobox = {k.lower(): v for k, v in infobox.items()}
    narrative = extract_narrative(lines, end_idx+1)
    # Extract world_id from 'world' or 'setting' (case-insensitive)
    world_id = infobox.get("world")
    if not world_id:
        # Try all keys for 'setting' (case-insensitive)
        setting = None
        for k in infobox:
            if k.startswith("setting"):
                setting = infobox[k]
                break
        if setting:
            m = re.search(r'\[\[([^\]|]+)\]\]', setting)
            if m:
                world_id = m.group(1)
            else:
                world_id = setting.split(',')[0].strip() if setting else None
            if world_id:
                world_id = world_id.lower().replace(' ', '_')
    book = {
        "id": infobox.get("title", Path(file_path).stem).lower().replace(' ', '_'),
        "title": infobox.get("title", Path(file_path).stem),
        "series_id": infobox.get("series"),
        "world_id": world_id,
        "publication_date": infobox.get("published"),
        "summary": narrative[:1000]
    }
    return book

def parse_character(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Find infobox (e.g., {{character}} or similar)
    infobox = None
    end_idx = 0
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('{{infobox character') or line.strip().lower().startswith('{{character'):
            infobox, end_idx = parse_infobox(lines, i+1)
            break
    if not infobox:
        infobox, end_idx = {"name": Path(file_path).stem}, 0
    # Lowercase all infobox keys for easier access
    infobox = {k.lower(): v for k, v in infobox.items()}
    narrative = extract_narrative(lines, end_idx+1)
    # Robust world_of_origin_id extraction
    world_of_origin_id = None
    for key in ["world", "planet", "homeworld"]:
        if key in infobox and infobox[key]:
            world_of_origin_id = infobox[key].lower().replace(' ', '_')
            break
    if not world_of_origin_id:
        # Try to find a world name in the biography using worlds.json
        try:
            with open("backend/data/worlds.json", "r") as wf:
                worlds = json.load(wf)
            world_names = [w["name"].lower() for w in worlds]
            for name in world_names:
                if name in narrative.lower():
                    world_of_origin_id = name.replace(' ', '_')
                    break
        except Exception:
            pass
    char = {
        "id": infobox.get("name", Path(file_path).stem).lower().replace(' ', '_'),
        "name": infobox.get("name", Path(file_path).stem),
        "aliases": [a.strip() for a in infobox.get("aliases", "").split(',') if a.strip()],
        "world_of_origin_id": world_of_origin_id,
        "species": infobox.get("species"),
        "status": infobox.get("status"),
        "biography": narrative[:1000]
    }
    return char

def parse_shard(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Find infobox
    infobox = None
    end_idx = 0
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('{{shard info'):
            infobox, end_idx = parse_infobox(lines, i+1)
            break
    if not infobox:
        infobox, end_idx = {"name": Path(file_path).stem}, 0
    infobox = {k.lower(): v for k, v in infobox.items()}
    narrative = extract_narrative(lines, end_idx+1)
    shard = {
        "id": infobox.get("name", Path(file_path).stem).lower().replace(' ', '_'),
        "name": infobox.get("name", Path(file_path).stem),
        "vessel": infobox.get("vessel"),
        "slivers": infobox.get("slivers"),
        "status": infobox.get("status"),
        "perpendicularity": infobox.get("perpendicularity"),
        "splinters": infobox.get("splinters"),
        "magic": infobox.get("magic"),
        "residence": infobox.get("residence"),
        "universe": infobox.get("universe"),
        "books": infobox.get("books"),
        "summary": narrative[:1000]
    }
    return shard

def parse_magic_system(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Find infobox
    infobox = None
    end_idx = 0
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('{{magic'):
            infobox, end_idx = parse_infobox(lines, i+1)
            break
    if not infobox:
        infobox, end_idx = {"name": Path(file_path).stem}, 0
    infobox = {k.lower(): v for k, v in infobox.items()}
    narrative = extract_narrative(lines, end_idx+1)
    magic = {
        "id": infobox.get("name", Path(file_path).stem).lower().replace(' ', '_'),
        "name": infobox.get("name", Path(file_path).stem),
        "related": infobox.get("related"),
        "universe": infobox.get("universe"),
        "summary": narrative[:1000]
    }
    return magic

def main():
    # Updated file paths for new test
    world_file = "/Users/jbthejedi/Documents/scadrial.html"
    book_file = "/Users/jbthejedi/Documents/mistborn_book_1.html"
    char_file = "/Users/jbthejedi/Documents/dalinar_kholin.html"
    out_dir = Path("backend/data")
    out_dir.mkdir(parents=True, exist_ok=True)
    # Parse and write
    world = parse_world(world_file)
    with open(out_dir / "worlds.json", "w") as f:
        json.dump([world], f, indent=2)
    book = parse_book(book_file)
    with open(out_dir / "books.json", "w") as f:
        json.dump([book], f, indent=2)
    char = parse_character(char_file)
    with open(out_dir / "characters.json", "w") as f:
        json.dump([char], f, indent=2)
    print("✅ Parsed and wrote worlds.json, books.json, characters.json")

if __name__ == "__main__":
    main() 