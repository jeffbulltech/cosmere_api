# backend/scripts/seed_database.py
import json
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import uuid
import re
import os

# Add the parent directory to the Python path to import from the root app
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.database import SessionLocal, create_tables, engine
from app.models import World, Series, Book, Character, Shard, MagicSystem
from app.core.config import SQLALCHEMY_DATABASE_URL

print("DATABASE_URL env:", os.getenv("DATABASE_URL"))
print("SQLALCHEMY_DATABASE_URL:", SQLALCHEMY_DATABASE_URL)
print("ACTUAL ENGINE URL AT SEED TIME:", engine.url)

class DatabaseSeeder:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.session: Session = None
    
    def load_json_data(self, filename: str) -> list:
        """Load data from JSON file"""
        file_path = self.data_dir / filename
        if not file_path.exists():
            print(f"Warning: {filename} not found, skipping...")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def seed_shards(self):
        print("🔮 Seeding Shards...")
        shards_data = self.load_json_data('shards.json')
        for shard_data in shards_data:
            shard = self.session.query(Shard).get(shard_data.get('id'))
            # Use 'title' as fallback for 'name'
            name = shard_data.get('name') or shard_data.get('title')
            # Use 'intent' if present, else try to extract from summary, else 'unknown'
            intent = shard_data.get('intent')
            if not intent:
                # Try to extract from summary (look for 'Intent' section)
                summary = shard_data.get('summary', '')
                m = re.search(r'==\s*intent\s*==\s*([^=]+)', summary, re.IGNORECASE)
                if m:
                    intent = m.group(1).strip().split('\n')[0]
                else:
                    intent = 'unknown'
            if shard:
                shard.name = name
                shard.intent = intent
                shard.vessel_name = shard_data.get('vessel_name')
                shard.vessel_status = shard_data.get('vessel_status', 'unknown')
                shard.description = shard_data.get('description', '')
            else:
                shard = Shard(
                    id=shard_data.get('id', str(uuid.uuid4())),
                    name=name,
                    intent=intent,
                    vessel_name=shard_data.get('vessel_name'),
                    vessel_status=shard_data.get('vessel_status', 'unknown'),
                    description=shard_data.get('description', '')
                )
                self.session.add(shard)
        self.session.commit()
        print(f"✅ Seeded {len(shards_data)} Shards")

    def seed_worlds(self):
        print("🌍 Seeding Worlds...")
        worlds_data = self.load_json_data('worlds.json')
        for world_data in worlds_data:
            world = self.session.query(World).get(world_data.get('id'))
            if world:
                world.name = world_data['name']
                world.system = world_data.get('system')
                world.geography = json.dumps(world_data.get('geography', {}))
                world.culture_notes = world_data.get('culture_notes')
                world.technology_level = world_data.get('technology_level')
            else:
                world = World(
                    id=world_data.get('id', str(uuid.uuid4())),
                    name=world_data['name'],
                    system=world_data.get('system'),
                    geography=json.dumps(world_data.get('geography', {})),
                    culture_notes=world_data.get('culture_notes'),
                    technology_level=world_data.get('technology_level')
                )
                self.session.add(world)
        self.session.commit()
        print(f"✅ Seeded {len(worlds_data)} Worlds")

    def seed_series(self):
        print("📚 Seeding Series...")
        series_data = self.load_json_data('series.json')
        for series_item in series_data:
            series = self.session.query(Series).get(series_item.get('id'))
            if series:
                series.name = series_item['name']
            else:
                series = Series(
                    id=series_item.get('id', str(uuid.uuid4())),
                    name=series_item['name']
                )
                self.session.add(series)
        self.session.commit()
        print(f"✅ Seeded {len(series_data)} Series")

    def seed_books(self):
        print("📖 Seeding Books...")
        books_data = self.load_json_data('books.json')
        for book_data in books_data:
            book = self.session.query(Book).get(book_data.get('id'))
            if book:
                book.title = book_data['title']
                book.series_id = book_data.get('series_id')
                book.world_id = book_data.get('world_id')
                book.publication_date = book_data.get('publication_date')
                book.chronological_order = book_data.get('chronological_order', 1)
                book.word_count = book_data.get('word_count')
                book.isbn = book_data.get('isbn')
                book.summary = book_data.get('summary')
                book.cosmere_significance = json.dumps(book_data.get('cosmere_significance', {}))
            else:
                book = Book(
                    id=book_data.get('id', str(uuid.uuid4())),
                    title=book_data['title'],
                    series_id=book_data.get('series_id'),
                    world_id=book_data.get('world_id'),
                    publication_date=book_data.get('publication_date'),
                    chronological_order=book_data.get('chronological_order', 1),
                    word_count=book_data.get('word_count'),
                    isbn=book_data.get('isbn'),
                    summary=book_data.get('summary'),
                    cosmere_significance=json.dumps(book_data.get('cosmere_significance', {}))
                )
                self.session.add(book)
        self.session.commit()
        print(f"✅ Seeded {len(books_data)} Books")

    def seed_characters(self):
        print("👥 Seeding Characters...")
        characters_data = self.load_json_data('characters.json')
        for char_data in characters_data:
            character = self.session.query(Character).get(char_data.get('id'))
            if character:
                character.name = char_data['name']
                character.aliases = json.dumps(char_data.get('aliases', []))
                character.world_of_origin_id = char_data.get('world_of_origin_id')
                character.species = char_data.get('species')
                character.magic_abilities = json.dumps(char_data.get('magic_abilities', {}))
                character.affiliations = json.dumps(char_data.get('affiliations', {}))
                character.status = char_data.get('status', 'unknown')
                character.first_appearance_book_id = char_data.get('first_appearance_book_id')
                character.biography = char_data.get('biography')
                character.cosmere_significance = json.dumps(char_data.get('cosmere_significance', {}))
            else:
                character = Character(
                    id=char_data.get('id', str(uuid.uuid4())),
                    name=char_data['name'],
                    aliases=json.dumps(char_data.get('aliases', [])),
                    world_of_origin_id=char_data.get('world_of_origin_id'),
                    species=char_data.get('species'),
                    magic_abilities=json.dumps(char_data.get('magic_abilities', {})),
                    affiliations=json.dumps(char_data.get('affiliations', {})),
                    status=char_data.get('status', 'unknown'),
                    first_appearance_book_id=char_data.get('first_appearance_book_id'),
                    biography=char_data.get('biography'),
                    cosmere_significance=json.dumps(char_data.get('cosmere_significance', {}))
                )
                self.session.add(character)
        self.session.commit()
        print(f"✅ Seeded {len(characters_data)} Characters")

    def seed_magic_systems(self):
        print("✨ Seeding Magic Systems...")
        magic_data = self.load_json_data('magic_systems.json')
        for magic_item in magic_data:
            magic_system = self.session.query(MagicSystem).get(magic_item.get('id'))
            # Use 'title' as fallback for 'name'
            name = magic_item.get('name') or magic_item.get('title')
            if magic_system:
                magic_system.name = name
                magic_system.related = magic_item.get('related')
                magic_system.universe = magic_item.get('universe')
                magic_system.description = magic_item.get('description', '')
            else:
                magic_system = MagicSystem(
                    id=magic_item.get('id', str(uuid.uuid4())),
                    name=name,
                    type=magic_item.get('type', 'unknown'),
                    power_source=magic_item.get('power_source'),
                    world_id=magic_item.get('world_id'),
                    description=magic_item.get('description', ''),
                    mechanics=magic_item.get('mechanics'),
                    limitations=magic_item.get('limitations')
                )
                self.session.add(magic_system)
        self.session.commit()
        print(f"✅ Seeded {len(magic_data)} Magic Systems")
    
    def run_seeding(self):
        """Run the complete seeding process"""
        # Create tables first
        create_tables()
        
        # Get database session
        self.session = SessionLocal()
        
        print("🌱 Starting Cosmere Database Seeding...")
        print("=" * 50)
        
        try:
            # Seed in dependency order
            self.seed_shards()
            self.seed_worlds()
            self.seed_series()
            self.seed_books()
            self.seed_characters()
            self.seed_magic_systems()
            
            print("=" * 50)
            print("🎉 Database seeding completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            self.session.rollback()
            raise
        finally:
            self.session.close()

def main():
    seeder = DatabaseSeeder()
    seeder.run_seeding()

if __name__ == "__main__":
    main()