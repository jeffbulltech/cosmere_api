// Core Cosmere entity types
export interface Character {
  id: string;
  name: string;
  aliases?: string; // JSON string from backend
  world_of_origin_id: string;
  species?: string;
  status?: string;
  first_appearance_book_id?: string;
  biography?: string;
  magic_abilities?: string; // JSON string from backend
  affiliations?: string; // JSON string from backend
  cosmere_significance?: string; // JSON string from backend
  created_at: string;
  updated_at: string;
  // Computed fields (added by frontend)
  book_count?: number;
  relationship_count?: number;
  has_magic_abilities?: boolean;
  is_alive?: boolean;
  magic_abilities_list?: string[];
  affiliations_list?: string[];
}

export interface Book {
  id: string;
  title: string;
  isbn?: string;
  publication_date?: string;
  word_count?: number;
  chronological_order?: number;
  series_id?: string;
  world_id: string;
  summary?: string;
  cosmere_significance?: string; // JSON string from backend
  created_at: string;
  updated_at: string;
}

export interface World {
  id: string;
  name: string;
  system?: string;
  shard_id?: string;
  geography?: string; // JSON string from backend
  culture_notes?: string;
  technology_level?: string;
  created_at: string;
  updated_at: string;
  // Computed fields (added by frontend)
  magic_systems?: Record<string, any>;
}

export interface MagicSystem {
  id: string;
  name: string;
  world_id?: string;
  type: string;
  power_source?: string;
  description?: string;
  mechanics?: string; // JSON string from backend
  limitations?: string; // JSON string from backend
  created_at: string;
  updated_at: string;
  // Computed fields (added by frontend)
  has_mechanics?: boolean;
  has_limitations?: boolean;
  mechanics_list?: string[];
  limitations_list?: string[];
}

export interface Series {
  id: string;
  name: string;
  description?: string;
  world_id?: string;
  status?: string;
  created_at: string;
  updated_at: string;
}

export interface Shard {
  id: string;
  name: string;
  intent: string;
  vessel_name?: string;
  vessel_status?: string;
  world_location_id?: string;
  description?: string;
  splinter_info?: string; // JSON string from backend
  created_at: string;
  updated_at: string;
}

export interface CharacterRelationship {
  id: string;
  character_id: string;
  related_character_id: string;
  relationship_type: string;
  description?: string;
  book_context_id?: string;
  created_at: string;
  updated_at: string;
}

// API Response types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  has_next: boolean;
  has_prev: boolean;
}

// Form types for creating/updating entities
export interface CharacterCreate {
  id: string;
  name: string;
  aliases?: string; // JSON string
  world_of_origin_id: string;
  species?: string;
  status?: string;
  first_appearance_book_id?: string;
  biography?: string;
  magic_abilities?: string; // JSON string
  affiliations?: string; // JSON string
  cosmere_significance?: string; // JSON string
}

export interface CharacterUpdate {
  name?: string;
  aliases?: string; // JSON string
  world_of_origin_id?: string;
  species?: string;
  status?: string;
  first_appearance_book_id?: string;
  biography?: string;
  magic_abilities?: string; // JSON string
  affiliations?: string; // JSON string
  cosmere_significance?: string; // JSON string
}

export interface BookCreate {
  id: string;
  title: string;
  world_id: string;
  series_id?: string;
  isbn?: string;
  publication_date?: string;
  word_count?: number;
  chronological_order?: number;
  summary?: string;
  cosmere_significance?: string; // JSON string
}

export interface BookUpdate {
  title?: string;
  world_id?: string;
  series_id?: string;
  isbn?: string;
  publication_date?: string;
  word_count?: number;
  chronological_order?: number;
  summary?: string;
  cosmere_significance?: string; // JSON string
}

export interface MagicSystemCreate {
  id: string;
  name: string;
  type: string;
  world_id: string;
  power_source?: string;
  description?: string;
  mechanics?: string; // JSON string
  limitations?: string; // JSON string
}

export interface MagicSystemUpdate {
  name?: string;
  type?: string;
  world_id?: string;
  power_source?: string;
  description?: string;
  mechanics?: string; // JSON string
  limitations?: string; // JSON string
}

// Filter types
export interface CharacterFilters {
  world_id?: string;
  status?: string;
  species?: string;
  magic_ability?: string;
  affiliation?: string;
  search?: string;
}

export interface BookFilters {
  series_id?: string;
  world_id?: string;
  publication_year?: number;
  search?: string;
}

export interface MagicSystemFilters {
  world_id?: string;
  type?: string;
  power_source?: string;
  search?: string;
}

// Search types
export interface SearchResult {
  id: string;
  name: string;
  type: 'character' | 'book' | 'world' | 'magic_system';
  description?: string;
  score?: number;
}

// Utility types for parsing JSON strings
export interface ParsedCharacter extends Omit<Character, 'aliases' | 'magic_abilities' | 'affiliations' | 'cosmere_significance'> {
  aliases?: string[] | null;
  magic_abilities?: Record<string, any> | null;
  affiliations?: Record<string, any> | null;
  cosmere_significance?: Record<string, any> | null;
}

export interface ParsedBook extends Omit<Book, 'cosmere_significance'> {
  cosmere_significance?: Record<string, any> | null;
}

export interface ParsedWorld extends Omit<World, 'geography'> {
  geography?: Record<string, any> | null;
}

export interface ParsedMagicSystem extends Omit<MagicSystem, 'mechanics' | 'limitations'> {
  mechanics?: Record<string, any> | null;
  limitations?: Record<string, any> | null;
}

export interface ParsedShard extends Omit<Shard, 'splinter_info'> {
  splinter_info?: Record<string, any> | null;
}
