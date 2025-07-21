import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import CosmereAPI from '../services/api';
import { Character, CharacterCreate, CharacterUpdate, CharacterFilters, PaginatedResponse } from '../types/cosmere';

// Query keys for React Query
export const characterKeys = {
  all: ['characters'] as const,
  lists: () => [...characterKeys.all, 'list'] as const,
  list: (filters: CharacterFilters) => [...characterKeys.lists(), filters] as const,
  details: () => [...characterKeys.all, 'detail'] as const,
  detail: (id: string) => [...characterKeys.details(), id] as const,
  relationships: (id: string) => [...characterKeys.detail(id), 'relationships'] as const,
  appearances: (id: string) => [...characterKeys.detail(id), 'appearances'] as const,
};

// Hook for fetching characters with pagination and filters
export const useCharacters = (params?: {
  skip?: number;
  limit?: number;
  world_id?: string;
  status?: string;
  species?: string;
  magic_ability?: string;
  search?: string;
}) => {
  return useQuery({
    queryKey: characterKeys.list(params || {}),
    queryFn: () => CosmereAPI.getCharacters(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for fetching a single character
export const useCharacter = (id: string) => {
  return useQuery({
    queryKey: characterKeys.detail(id),
    queryFn: () => CosmereAPI.getCharacter(id),
    enabled: !!id,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Hook for fetching character relationships
export const useCharacterRelationships = (id: string) => {
  return useQuery({
    queryKey: characterKeys.relationships(id),
    queryFn: () => CosmereAPI.getCharacterRelationships(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for fetching character appearances
export const useCharacterAppearances = (id: string) => {
  return useQuery({
    queryKey: characterKeys.appearances(id),
    queryFn: () => CosmereAPI.getCharacterAppearances(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for creating a character
export const useCreateCharacter = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (characterData: CharacterCreate) => CosmereAPI.createCharacter(characterData),
    onSuccess: () => {
      // Invalidate and refetch character lists
      queryClient.invalidateQueries({ queryKey: characterKeys.lists() });
    },
  });
};

// Hook for updating a character
export const useUpdateCharacter = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: CharacterUpdate }) =>
      CosmereAPI.updateCharacter(id, data),
    onSuccess: (updatedCharacter) => {
      // Update the character in cache
      queryClient.setQueryData(characterKeys.detail(updatedCharacter.id), updatedCharacter);
      // Invalidate character lists
      queryClient.invalidateQueries({ queryKey: characterKeys.lists() });
    },
  });
};

// Hook for deleting a character
export const useDeleteCharacter = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => CosmereAPI.deleteCharacter(id),
    onSuccess: (_, deletedId) => {
      // Remove character from cache
      queryClient.removeQueries({ queryKey: characterKeys.detail(deletedId) });
      // Invalidate character lists
      queryClient.invalidateQueries({ queryKey: characterKeys.lists() });
    },
  });
};

// Hook for searching characters
export const useSearchCharacters = (
  query: string,
  filters?: CharacterFilters,
  size: number = 20
) => {
  return useQuery({
    queryKey: ['characters', 'search', query, filters, size],
    queryFn: () => CosmereAPI.searchCharacters(query, filters, size),
    enabled: !!query && query.length >= 2,
    staleTime: 2 * 60 * 1000, // 2 minutes for search results
  });
};

// Hook for getting characters by world
export const useCharactersByWorld = (worldId: string) => {
  return useQuery({
    queryKey: ['characters', 'world', worldId],
    queryFn: () => CosmereAPI.getCharacters({ world_id: worldId }),
    enabled: !!worldId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for getting characters by status
export const useCharactersByStatus = (status: string) => {
  return useQuery({
    queryKey: ['characters', 'status', status],
    queryFn: () => CosmereAPI.getCharacters({ status }),
    enabled: !!status,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}; 