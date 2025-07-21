// Core Cosmere entity types
export interface Character {
  id: string;
  name: string;
  aliases: string[];
  world_of_origin: World;
  species?: string;
  magic_abilities: Record<string, any>;
  affiliations: Record<string, any>;
  status: 'alive' | 'dead' | 'cognitive_shadow' | 'unknown';
  first_appearance_book?: Book;
  biography?: string;
  cosmere_significance?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface World {
  id: string;
  name: string;
  system?: string;
  shard?: Shard;
  magic_systems: MagicSystem[];
  geography: Record<string, any>;
  culture_notes?: string;
  technology_level?: string;
  created_at: string;
  updated_at: string;
}

export interface Book {
  id: string;
  title: string;
  series?: Series;
  world: World;
  publication_date: string;
  chronological_order: number;
  word_count?: number;
  isbn?: string;
  summary?: string;
  cosmere_significance?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Series {
  id: string;
  name: string;
  description?: string;
  books: Book[];
  created_at: string;
  updated_at: string;
}

export interface MagicSystem {
  id: string;
  name: string;
  world: World;
  type: string; // allomancy, feruchemy, hemalurgy, surgebinding, etc.
  mechanics: Record<string, any>;
  limitations: Record<string, any>;
  power_source?: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Shard {
  id: string;
  name: string;
  intent: string;
  vessel_name?: string;
  vessel_status?: string;
  world_location?: World;
  splinter_info?: Record<string, any>;
  description?: string;
  created_at: string;
  updated_at: string;
}

// Relationship types
export interface CharacterRelationship {
  character_id: string;
  related_character_id: string;
  relationship_type: string;
  description?: string;
  book_context?: Book;
}

export interface CharacterBook {
  character_id: string;
  book_id: string;
  role: 'protagonist' | 'antagonist' | 'supporting' | 'minor';
}

// Search and API response types
export interface SearchResult<T> {
  items: T[];
  total: number;
  query: string;
  took: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface ApiResponse<T> {
  data: T;
  meta: {
    timestamp: string;
    version: string;
  };
}

// Filter and query types
export interface CharacterFilters {
  world_id?: string;
  status?: string;
  species?: string;
  magic_ability?: string;
}

export interface BookFilters {
  series_id?: string;
  world_id?: string;
  publication_year?: number;
}

export interface WorldFilters {
  system?: string;
  technology_level?: string;
  has_shard?: boolean;
}

// Timeline and analysis types
export interface TimelineEvent {
  id: string;
  title: string;
  description: string;
  date?: string;
  world: World;
  books: Book[];
  characters: Character[];
  event_type: 'battle' | 'discovery' | 'birth' | 'death' | 'political' | 'other';
}

export interface CrossReference {
  entity_id: string;
  entity_type: 'character' | 'magic_system' | 'organization';
  appearances: Book[];
  worlds: World[];
  significance: string;
}

// Form types for creating/updating entities
export interface CharacterCreate {
  name: string;
  aliases?: string[];
  world_of_origin_id: string;
  species?: string;
  status?: string;
  biography?: string;
}

export interface CharacterUpdate {
  name?: string;
  aliases?: string[];
  world_of_origin_id?: string;
  species?: string;
  status?: string;
  biography?: string;
  magic_abilities?: Record<string, any>;
  affiliations?: Record<string, any>;
}

export interface BookCreate {
  title: string;
  series_id?: string;
  world_id: string;
  publication_date: string;
  chronological_order: number;
  summary?: string;
}

export interface WorldCreate {
  name: string;
  system?: string;
  geography?: Record<string, any>;
  culture_notes?: string;
  technology_level?: string;
} 