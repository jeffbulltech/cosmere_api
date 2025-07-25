# Database Schema Documentation

## Overview

The Cosmere API database is designed to represent the complex relationships within Brandon Sanderson's Cosmere universe. The schema supports books, characters, worlds, magic systems, and their interconnections.

## Entity Relationship Diagram

```
Worlds (1) ←→ (N) Series
Worlds (1) ←→ (N) Books  
Worlds (1) ←→ (N) Characters
Worlds (1) ←→ (N) Magic Systems

Series (1) ←→ (N) Books

Books (N) ←→ (N) Characters (via BookCharacter)
Characters (N) ←→ (N) Characters (via CharacterRelationship)
Characters (N) ←→ (N) Magic Systems (via CharacterMagicSystem)

Shards (1) ←→ (N) ShardVessels
```

## Tables

### Core Entities

#### 1. Worlds
Represents the various planets and locations in the Cosmere.

**Fields:**
- `id` (String, PK): Unique identifier
- `name` (String): World name
- `description` (Text): World description
- `system` (String): Planetary system
- `is_habitable` (Boolean): Whether the world is habitable
- `magic_systems_description` (Text): Description of magic systems
- `notable_features` (Text): Notable features of the world
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Has many Series
- Has many Books
- Has many Characters
- Has many Magic Systems

#### 2. Series
Represents book series within the Cosmere.

**Fields:**
- `id` (String, PK): Unique identifier
- `name` (String): Series name
- `description` (Text): Series description
- `world_id` (String, FK): Reference to World
- `planned_books` (Integer): Number of planned books
- `current_books` (Integer): Number of published books
- `status` (Enum): ongoing, complete, planned, on_hiatus
- `reading_order` (Text): JSON string for reading order
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Belongs to World
- Has many Books

#### 3. Books
Represents individual books in the Cosmere.

**Fields:**
- `id` (String, PK): Unique identifier
- `title` (String): Book title
- `series_id` (String, FK): Reference to Series
- `world_id` (String, FK): Reference to World
- `publication_date` (Date): Publication date
- `summary` (Text): Book summary
- `page_count` (Integer): Number of pages
- `is_standalone` (Boolean): Whether it's a standalone book
- `reading_order` (Integer): Order within series
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Belongs to Series
- Belongs to World
- Has many Characters (via BookCharacter)

#### 4. Characters
Represents characters in the Cosmere.

**Fields:**
- `id` (String, PK): Unique identifier
- `name` (String): Character name
- `aliases` (Array[String]): Array of alias names
- `world_of_origin_id` (String, FK): Reference to World
- `species` (String): Character species
- `status` (Enum): alive, dead, unknown, immortal
- `biography` (Text): Character biography
- `appearance` (Text): Physical appearance
- `personality` (Text): Personality description
- `abilities` (Text): Character abilities
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Belongs to World
- Has many Books (via BookCharacter)
- Has many Relationships (via CharacterRelationship)
- Has many Magic Systems (via CharacterMagicSystem)

#### 5. Magic Systems
Represents magic systems in the Cosmere.

**Fields:**
- `id` (String, PK): Unique identifier
- `name` (String): Magic system name
- `world_id` (String, FK): Reference to World
- `description` (Text): System description
- `mechanics` (Text): How the magic works
- `requirements` (Text): Requirements to use
- `limitations` (Text): System limitations
- `is_investiture_based` (Boolean): Whether it's investiture-based
- `related_systems` (Text): JSON string of related systems
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Belongs to World
- Has many Characters (via CharacterMagicSystem)

#### 6. Shards
Represents Shards of Adonalsium.

**Fields:**
- `id` (String, PK): Unique identifier
- `name` (String): Shard name
- `intent` (String): The Shard's intent
- `status` (Enum): whole, splintered, conjoined, unknown
- `current_vessel` (String): Current vessel name
- `original_vessel` (String): Original vessel name
- `description` (Text): Shard description
- `perpendicularity` (Text): Location of perpendicularity
- `magic_systems` (Text): Associated magic systems
- `residence` (Text): Where the Shard resides
- `is_combined` (Boolean): Is this a combination of Shards
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Has many ShardVessels

### Junction Tables

#### 7. BookCharacter
Many-to-many relationship between Books and Characters.

**Fields:**
- `id` (String, PK): Unique identifier
- `book_id` (String, FK): Reference to Book
- `character_id` (String, FK): Reference to Character
- `role` (String): Character role in book
- `is_pov_character` (Boolean): Is this a POV character
- `first_appearance` (Boolean): Is this their first appearance
- `notes` (Text): Additional notes
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

#### 8. CharacterRelationship
Many-to-many relationship between Characters.

**Fields:**
- `id` (String, PK): Unique identifier
- `character_id` (String, FK): Reference to Character
- `related_character_id` (String, FK): Reference to related Character
- `relationship_type` (Enum): family, romantic, friendship, enemy, mentor, student, ally, rival, other
- `description` (Text): Relationship description
- `is_reciprocal` (Boolean): Is this relationship mutual
- `strength` (String): Relationship strength
- `notes` (Text): Additional notes
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

#### 9. CharacterMagicSystem
Many-to-many relationship between Characters and Magic Systems.

**Fields:**
- `id` (String, PK): Unique identifier
- `character_id` (String, FK): Reference to Character
- `magic_system_id` (String, FK): Reference to Magic System
- `user_type` (Enum): practitioner, student, former, potential, unknown
- `proficiency_level` (String): Skill level
- `is_active` (Boolean): Is currently using this magic
- `notes` (Text): Additional notes
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

#### 10. ShardVessel
Represents vessels of Shards.

**Fields:**
- `id` (String, PK): Unique identifier
- `shard_id` (String, FK): Reference to Shard
- `vessel_name` (String): Vessel name
- `vessel_type` (String): original, current, former
- `start_date` (String): When they became vessel
- `end_date` (String): When they stopped being vessel
- `description` (Text): Vessel description
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

## Indexes

The following indexes are created for performance:

- Primary keys on all tables
- Foreign key indexes on all relationship fields
- Name indexes on searchable fields (World.name, Character.name, etc.)
- Status indexes on enum fields
- Composite indexes for common query patterns

## Data Integrity

### Foreign Key Constraints
- All foreign key relationships are properly constrained
- Cascade delete rules are applied where appropriate
- Nullable foreign keys for optional relationships

### Check Constraints
- Enum values are validated at the database level
- Boolean fields have proper constraints
- String length limits are enforced

### Unique Constraints
- Unique constraints on business keys where appropriate
- Composite unique constraints for junction tables

## Query Patterns

### Common Queries

1. **Get all characters in a book:**
   ```sql
   SELECT c.* FROM characters c
   JOIN book_characters bc ON c.id = bc.character_id
   WHERE bc.book_id = ?
   ```

2. **Get all books in a series:**
   ```sql
   SELECT * FROM books WHERE series_id = ? ORDER BY reading_order
   ```

3. **Get character relationships:**
   ```sql
   SELECT cr.*, c1.name as character_name, c2.name as related_name
   FROM character_relationships cr
   JOIN characters c1 ON cr.character_id = c1.id
   JOIN characters c2 ON cr.related_character_id = c2.id
   WHERE cr.character_id = ?
   ```

4. **Get magic system users:**
   ```sql
   SELECT c.* FROM characters c
   JOIN character_magic_systems cms ON c.id = cms.character_id
   WHERE cms.magic_system_id = ? AND cms.is_active = true
   ```

## Migration Strategy

1. **Initial Migration:** Creates all tables with proper relationships
2. **Data Migration:** Imports data from JSON files
3. **Index Optimization:** Adds performance indexes
4. **Constraint Validation:** Ensures data integrity

## Future Considerations

- **Full-text Search:** Consider adding full-text search capabilities
- **Audit Trail:** Add audit tables for tracking changes
- **Soft Deletes:** Implement soft delete functionality
- **Caching:** Add caching layer for frequently accessed data
- **Partitioning:** Consider table partitioning for large datasets 