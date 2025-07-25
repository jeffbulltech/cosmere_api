import { 
  Character, Book, World, MagicSystem, Series, Shard,
  CharacterCreate, CharacterUpdate, BookCreate, BookUpdate, MagicSystemCreate, MagicSystemUpdate,
  PaginatedResponse, CharacterFilters, BookFilters, MagicSystemFilters, SearchResult
} from '../types/cosmere';

const API_BASE = '/api/v1';

// Generic API helper
async function apiRequest<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });
  
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
}

// Books API
export async function fetchBooks(filters?: BookFilters): Promise<PaginatedResponse<Book>> {
  const params = new URLSearchParams();
  if (filters?.series_id) params.append('series_id', filters.series_id);
  if (filters?.world_id) params.append('world_id', filters.world_id);
  if (filters?.publication_year) params.append('publication_year', filters.publication_year.toString());
  if (filters?.search) params.append('search', filters.search);
  
  return apiRequest<PaginatedResponse<Book>>(`/books/?${params.toString()}`);
}

export async function fetchBook(id: string): Promise<Book> {
  return apiRequest<Book>(`/books/${id}`);
}

export async function createBook(book: BookCreate): Promise<Book> {
  return apiRequest<Book>('/books/', {
    method: 'POST',
    body: JSON.stringify(book),
  });
}

export async function updateBook(id: string, book: BookUpdate): Promise<Book> {
  return apiRequest<Book>(`/books/${id}`, {
    method: 'PUT',
    body: JSON.stringify(book),
  });
}

export async function deleteBook(id: string): Promise<void> {
  return apiRequest<void>(`/books/${id}`, {
    method: 'DELETE',
  });
}

// Characters API
export async function fetchCharacters(filters?: CharacterFilters): Promise<PaginatedResponse<Character>> {
  const params = new URLSearchParams();
  if (filters?.world_id) params.append('world_id', filters.world_id);
  if (filters?.status) params.append('status', filters.status);
  if (filters?.species) params.append('species', filters.species);
  if (filters?.magic_ability) params.append('magic_ability', filters.magic_ability);
  if (filters?.affiliation) params.append('affiliation', filters.affiliation);
  if (filters?.search) params.append('search', filters.search);
  
  return apiRequest<PaginatedResponse<Character>>(`/characters/?${params.toString()}`);
}

export async function fetchCharacter(id: string): Promise<Character> {
  return apiRequest<Character>(`/characters/${id}`);
}

export async function createCharacter(character: CharacterCreate): Promise<Character> {
  return apiRequest<Character>('/characters/', {
    method: 'POST',
    body: JSON.stringify(character),
  });
}

export async function updateCharacter(id: string, character: CharacterUpdate): Promise<Character> {
  return apiRequest<Character>(`/characters/${id}`, {
    method: 'PUT',
    body: JSON.stringify(character),
  });
}

export async function deleteCharacter(id: string): Promise<void> {
  return apiRequest<void>(`/characters/${id}`, {
    method: 'DELETE',
  });
}

// Worlds API
export async function fetchWorlds(): Promise<PaginatedResponse<World>> {
  return apiRequest<PaginatedResponse<World>>('/worlds/');
}

export async function fetchWorld(id: string): Promise<World> {
  return apiRequest<World>(`/worlds/${id}`);
}

export async function createWorld(world: any): Promise<World> {
  return apiRequest<World>('/worlds/', {
    method: 'POST',
    body: JSON.stringify(world),
  });
}

export async function updateWorld(id: string, world: any): Promise<World> {
  return apiRequest<World>(`/worlds/${id}`, {
    method: 'PUT',
    body: JSON.stringify(world),
  });
}

export async function deleteWorld(id: string): Promise<void> {
  return apiRequest<void>(`/worlds/${id}`, {
    method: 'DELETE',
  });
}

// Magic Systems API
export async function fetchMagicSystems(filters?: MagicSystemFilters): Promise<PaginatedResponse<MagicSystem>> {
  const params = new URLSearchParams();
  if (filters?.world_id) params.append('world_id', filters.world_id);
  if (filters?.type) params.append('type', filters.type);
  if (filters?.power_source) params.append('power_source', filters.power_source);
  if (filters?.search) params.append('search', filters.search);
  
  return apiRequest<PaginatedResponse<MagicSystem>>(`/magic-systems/?${params.toString()}`);
}

export async function fetchMagicSystem(id: string): Promise<MagicSystem> {
  return apiRequest<MagicSystem>(`/magic-systems/${id}`);
}

export async function createMagicSystem(magicSystem: MagicSystemCreate): Promise<MagicSystem> {
  return apiRequest<MagicSystem>('/magic-systems/', {
    method: 'POST',
    body: JSON.stringify(magicSystem),
  });
}

export async function updateMagicSystem(id: string, magicSystem: MagicSystemUpdate): Promise<MagicSystem> {
  return apiRequest<MagicSystem>(`/magic-systems/${id}`, {
    method: 'PUT',
    body: JSON.stringify(magicSystem),
  });
}

export async function deleteMagicSystem(id: string): Promise<void> {
  return apiRequest<void>(`/magic-systems/${id}`, {
    method: 'DELETE',
  });
}

// Series API
export async function fetchSeries(): Promise<PaginatedResponse<Series>> {
  return apiRequest<PaginatedResponse<Series>>('/series/');
}

export async function fetchSeriesById(id: string): Promise<Series> {
  return apiRequest<Series>(`/series/${id}`);
}

export async function createSeries(series: any): Promise<Series> {
  return apiRequest<Series>('/series/', {
    method: 'POST',
    body: JSON.stringify(series),
  });
}

export async function updateSeries(id: string, series: any): Promise<Series> {
  return apiRequest<Series>(`/series/${id}`, {
    method: 'PUT',
    body: JSON.stringify(series),
  });
}

export async function deleteSeries(id: string): Promise<void> {
  return apiRequest<void>(`/series/${id}`, {
    method: 'DELETE',
  });
}

// Shards API
export async function fetchShards(): Promise<PaginatedResponse<Shard>> {
  return apiRequest<PaginatedResponse<Shard>>('/shards/');
}

export async function fetchShard(id: string): Promise<Shard> {
  return apiRequest<Shard>(`/shards/${id}`);
}

export async function createShard(shard: any): Promise<Shard> {
  return apiRequest<Shard>('/shards/', {
    method: 'POST',
    body: JSON.stringify(shard),
  });
}

export async function updateShard(id: string, shard: any): Promise<Shard> {
  return apiRequest<Shard>(`/shards/${id}`, {
    method: 'PUT',
    body: JSON.stringify(shard),
  });
}

export async function deleteShard(id: string): Promise<void> {
  return apiRequest<void>(`/shards/${id}`, {
    method: 'DELETE',
  });
}

// Search API
export async function searchGlobal(query: string): Promise<SearchResult[]> {
  return apiRequest<SearchResult[]>(`/search/global?q=${encodeURIComponent(query)}`);
}

export async function searchCharacters(query: string): Promise<SearchResult[]> {
  return apiRequest<SearchResult[]>(`/search/characters?q=${encodeURIComponent(query)}`);
}
