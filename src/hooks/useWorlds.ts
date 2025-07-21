import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import CosmereAPI from '../services/api';
import { World, WorldCreate, WorldFilters, PaginatedResponse } from '../types/cosmere';

// Query keys for React Query
export const worldKeys = {
  all: ['worlds'] as const,
  lists: () => [...worldKeys.all, 'list'] as const,
  list: (filters: WorldFilters) => [...worldKeys.lists(), filters] as const,
  details: () => [...worldKeys.all, 'detail'] as const,
  detail: (id: string) => [...worldKeys.details(), id] as const,
  characters: (worldId: string) => [...worldKeys.detail(worldId), 'characters'] as const,
  magicSystems: (worldId: string) => [...worldKeys.detail(worldId), 'magic-systems'] as const,
};

// Hook for fetching worlds with pagination and filters
export const useWorlds = (params?: {
  skip?: number;
  limit?: number;
  system?: string;
  technology_level?: string;
  has_shard?: boolean;
}) => {
  return useQuery({
    queryKey: worldKeys.list(params || {}),
    queryFn: () => CosmereAPI.getWorlds(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for fetching a single world
export const useWorld = (id: string) => {
  return useQuery({
    queryKey: worldKeys.detail(id),
    queryFn: () => CosmereAPI.getWorld(id),
    enabled: !!id,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Hook for fetching characters from a world
export const useWorldCharacters = (worldId: string) => {
  return useQuery({
    queryKey: worldKeys.characters(worldId),
    queryFn: () => CosmereAPI.getWorldCharacters(worldId),
    enabled: !!worldId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for fetching magic systems from a world
export const useWorldMagicSystems = (worldId: string) => {
  return useQuery({
    queryKey: worldKeys.magicSystems(worldId),
    queryFn: () => CosmereAPI.getWorldMagicSystems(worldId),
    enabled: !!worldId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for creating a world
export const useCreateWorld = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (worldData: WorldCreate) => CosmereAPI.createWorld(worldData),
    onSuccess: () => {
      // Invalidate and refetch world lists
      queryClient.invalidateQueries({ queryKey: worldKeys.lists() });
    },
  });
};

// Hook for updating a world
export const useUpdateWorld = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<WorldCreate> }) =>
      CosmereAPI.updateWorld(id, data),
    onSuccess: (updatedWorld: World) => {
      // Update the world in cache
      queryClient.setQueryData(worldKeys.detail(updatedWorld.id), updatedWorld);
      // Invalidate world lists
      queryClient.invalidateQueries({ queryKey: worldKeys.lists() });
    },
  });
};

// Hook for deleting a world
export const useDeleteWorld = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => CosmereAPI.deleteWorld(id),
    onSuccess: (_: void, deletedId: string) => {
      // Remove world from cache
      queryClient.removeQueries({ queryKey: worldKeys.detail(deletedId) });
      // Invalidate world lists
      queryClient.invalidateQueries({ queryKey: worldKeys.lists() });
    },
  });
};

// Hook for searching worlds
export const useSearchWorlds = (
  query: string,
  filters?: WorldFilters,
  size: number = 20
) => {
  return useQuery({
    queryKey: ['worlds', 'search', query, filters, size],
    queryFn: () => CosmereAPI.searchWorlds(query, filters, size),
    enabled: !!query && query.length >= 2,
    staleTime: 2 * 60 * 1000, // 2 minutes for search results
  });
}; 