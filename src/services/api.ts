import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  Character,
  World,
  Book,
  Series,
  MagicSystem,
  SearchResult,
  PaginatedResponse,
  CharacterFilters,
  BookFilters,
  WorldFilters,
  CharacterCreate,
  CharacterUpdate,
  BookCreate,
  WorldCreate,
  CharacterRelationship,
  TimelineEvent,
  CrossReference
} from '../types/cosmere';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5240/api/v1';

// Create axios instance with default configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export class CosmereAPI {
  // Character endpoints
  static async getCharacters(params?: {
    skip?: number;
    limit?: number;
    world_id?: string;
    status?: string;
    species?: string;
    magic_ability?: string;
    search?: string;
  }): Promise<PaginatedResponse<Character>> {
    const response = await apiClient.get('/characters', { params });
    return response.data;
  }

  static async getCharacter(id: string): Promise<Character> {
    const response = await apiClient.get(`/characters/${id}`);
    return response.data;
  }

  static async createCharacter(characterData: CharacterCreate): Promise<Character> {
    const response = await apiClient.post('/characters', characterData);
    return response.data;
  }

  static async updateCharacter(id: string, characterData: CharacterUpdate): Promise<Character> {
    const response = await apiClient.put(`/characters/${id}`, characterData);
    return response.data;
  }

  static async deleteCharacter(id: string): Promise<void> {
    await apiClient.delete(`/characters/${id}`);
  }

  static async getCharacterRelationships(id: string): Promise<CharacterRelationship[]> {
    const response = await apiClient.get(`/characters/${id}/relationships`);
    return response.data;
  }

  static async getCharacterAppearances(id: string): Promise<Book[]> {
    const response = await apiClient.get(`/characters/${id}/appearances`);
    return response.data;
  }

  // Book endpoints
  static async getBooks(params?: {
    skip?: number;
    limit?: number;
    series_id?: string;
    world_id?: string;
    publication_year?: number;
  }): Promise<PaginatedResponse<Book>> {
    const response = await apiClient.get('/books', { params });
    return response.data;
  }

  static async getBook(id: string): Promise<Book> {
    const response = await apiClient.get(`/books/${id}`);
    return response.data;
  }

  static async createBook(bookData: BookCreate): Promise<Book> {
    const response = await apiClient.post('/books', bookData);
    return response.data;
  }

  static async updateBook(id: string, bookData: Partial<BookCreate>): Promise<Book> {
    const response = await apiClient.put(`/books/${id}`, bookData);
    return response.data;
  }

  static async deleteBook(id: string): Promise<void> {
    await apiClient.delete(`/books/${id}`);
  }

  static async getBooksBySeries(seriesId: string): Promise<Book[]> {
    const response = await apiClient.get(`/books/series/${seriesId}`);
    return response.data;
  }

  static async getBooksByWorld(worldId: string): Promise<Book[]> {
    const response = await apiClient.get(`/books/world/${worldId}`);
    return response.data;
  }

  // World endpoints
  static async getWorlds(params?: {
    skip?: number;
    limit?: number;
    system?: string;
    technology_level?: string;
    has_shard?: boolean;
  }): Promise<PaginatedResponse<World>> {
    const response = await apiClient.get('/worlds', { params });
    return response.data;
  }

  static async getWorld(id: string): Promise<World> {
    const response = await apiClient.get(`/worlds/${id}`);
    return response.data;
  }

  static async createWorld(worldData: WorldCreate): Promise<World> {
    const response = await apiClient.post('/worlds', worldData);
    return response.data;
  }

  static async updateWorld(id: string, worldData: Partial<WorldCreate>): Promise<World> {
    const response = await apiClient.put(`/worlds/${id}`, worldData);
    return response.data;
  }

  static async deleteWorld(id: string): Promise<void> {
    await apiClient.delete(`/worlds/${id}`);
  }

  static async getWorldCharacters(worldId: string): Promise<Character[]> {
    const response = await apiClient.get(`/worlds/${worldId}/characters`);
    return response.data;
  }

  static async getWorldMagicSystems(worldId: string): Promise<MagicSystem[]> {
    const response = await apiClient.get(`/worlds/${worldId}/magic-systems`);
    return response.data;
  }

  // Magic System endpoints
  static async getMagicSystems(params?: {
    skip?: number;
    limit?: number;
    world_id?: string;
    type?: string;
  }): Promise<PaginatedResponse<MagicSystem>> {
    const response = await apiClient.get('/magic-systems', { params });
    return response.data;
  }

  static async getMagicSystem(id: string): Promise<MagicSystem> {
    const response = await apiClient.get(`/magic-systems/${id}`);
    return response.data;
  }

  static async getMagicSystemsByWorld(worldId: string): Promise<MagicSystem[]> {
    const response = await apiClient.get(`/magic-systems/world/${worldId}`);
    return response.data;
  }

  // Series endpoints
  static async getSeries(): Promise<Series[]> {
    const response = await apiClient.get('/series');
    return response.data;
  }

  static async getSeriesById(id: string): Promise<Series> {
    const response = await apiClient.get(`/series/${id}`);
    return response.data;
  }

  // Search endpoints
  static async searchCharacters(
    query: string,
    filters?: CharacterFilters,
    size: number = 20
  ): Promise<SearchResult<Character>> {
    const response = await apiClient.get('/search/characters', {
      params: { q: query, size, ...filters }
    });
    return response.data;
  }

  static async searchBooks(
    query: string,
    filters?: BookFilters,
    size: number = 20
  ): Promise<SearchResult<Book>> {
    const response = await apiClient.get('/search/books', {
      params: { q: query, size, ...filters }
    });
    return response.data;
  }

  static async searchWorlds(
    query: string,
    filters?: WorldFilters,
    size: number = 20
  ): Promise<SearchResult<World>> {
    const response = await apiClient.get('/search/worlds', {
      params: { q: query, size, ...filters }
    });
    return response.data;
  }

  static async globalSearch(query: string, size: number = 20): Promise<SearchResult<any>> {
    const response = await apiClient.get('/search/global', {
      params: { q: query, size }
    });
    return response.data;
  }

  // Analysis and cross-reference endpoints
  static async getCrossReferences(
    entityType: 'character' | 'magic_system' | 'organization'
  ): Promise<CrossReference[]> {
    const response = await apiClient.get('/cross-references', {
      params: { entity_type: entityType }
    });
    return response.data;
  }

  static async getTimeline(worldId?: string): Promise<TimelineEvent[]> {
    const response = await apiClient.get('/timeline', {
      params: { world_id: worldId }
    });
    return response.data;
  }

  static async getConnections(): Promise<any> {
    const response = await apiClient.get('/connections');
    return response.data;
  }

  // Health check
  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await apiClient.get('/health');
    return response.data;
  }
}

// Export the apiClient instance for direct use if needed
export { apiClient };

// Export default instance
export default CosmereAPI; 