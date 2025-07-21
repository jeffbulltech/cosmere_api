# backend/scripts/merge_data_sources.py
import json
from pathlib import Path
from typing import Dict, List

class DataMerger:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
    
    def merge_character_data(self):
        """Merge manual JSON data with Coppermind data"""
        
        # Load manual data
        manual_chars = self.load_json('characters.json')
        coppermind_chars = self.load_json('coppermind_characters.json')
        
        # Create lookup dictionary
        manual_lookup = {char['name'].lower(): char for char in manual_chars}
        
        # Enhance with Coppermind data
        for cm_char in coppermind_chars:
            name_key = cm_char['name'].lower()
            if name_key in manual_lookup:
                # Merge data
                manual_lookup[name_key]['biography'] = cm_char.get('summary', '')
                manual_lookup[name_key]['categories'] = cm_char.get('categories', [])
            else:
                # Add new character from Coppermind
                new_char = {
                    'name': cm_char['name'],
                    'biography': cm_char.get('summary', ''),
                    'categories': cm_char.get('categories', []),
                    'status': 'unknown',
                    'world_of_origin_id': self.guess_world_from_categories(cm_char.get('categories', []))
                }
                manual_chars.append(new_char)
        
        # Save merged data (overwrite characters.json and also keep characters_merged.json for backup)
        self.save_json('characters.json', manual_chars)
        self.save_json('characters_merged.json', manual_chars)
        print(f"✅ Merged character data: {len(manual_chars)} total characters (characters.json updated)")
    
    def guess_world_from_categories(self, categories: List[str]) -> str:
        """Guess world based on wiki categories"""
        for category in categories:
            if 'Roshar' in category or 'Stormlight' in category:
                return 'roshar'
            elif 'Scadrial' in category or 'Mistborn' in category:
                return 'scadrial'
            elif 'Nalthis' in category or 'Warbreaker' in category:
                return 'nalthis'
        return None
    
    def load_json(self, filename: str) -> List:
        file_path = self.data_dir / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_json(self, filename: str, data: List):
        file_path = self.data_dir / filename
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    merger = DataMerger()
    merger.merge_character_data()