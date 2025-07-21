import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import CosmereAPI from '../services/api';
import { Book, BookCreate, BookFilters, PaginatedResponse } from '../types/cosmere';

// Query keys for React Query
export const bookKeys = {
  all: ['books'] as const,
  lists: () => [...bookKeys.all, 'list'] as const,
  list: (filters: BookFilters) => [...bookKeys.lists(), filters] as const,
  details: () => [...bookKeys.all, 'detail'] as const,
  detail: (id: string) => [...bookKeys.details(), id] as const,
  series: (seriesId: string) => [...bookKeys.all, 'series', seriesId] as const,
  world: (worldId: string) => [...bookKeys.all, 'world', worldId] as const,
};

// Hook for fetching books with pagination and filters
export const useBooks = (params?: {
  skip?: number;
  limit?: number;
  series_id?: string;
  world_id?: string;
  publication_year?: number;
}) => {
  return useQuery({
    queryKey: bookKeys.list(params || {}),
    queryFn: () => CosmereAPI.getBooks(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for fetching a single book
export const useBook = (id: string) => {
  return useQuery({
    queryKey: bookKeys.detail(id),
    queryFn: () => CosmereAPI.getBook(id),
    enabled: !!id,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Hook for fetching books by series
export const useBooksBySeries = (seriesId: string) => {
  return useQuery({
    queryKey: bookKeys.series(seriesId),
    queryFn: () => CosmereAPI.getBooksBySeries(seriesId),
    enabled: !!seriesId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for fetching books by world
export const useBooksByWorld = (worldId: string) => {
  return useQuery({
    queryKey: bookKeys.world(worldId),
    queryFn: () => CosmereAPI.getBooksByWorld(worldId),
    enabled: !!worldId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for creating a book
export const useCreateBook = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (bookData: BookCreate) => CosmereAPI.createBook(bookData),
    onSuccess: () => {
      // Invalidate and refetch book lists
      queryClient.invalidateQueries({ queryKey: bookKeys.lists() });
    },
  });
};

// Hook for updating a book
export const useUpdateBook = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<BookCreate> }) =>
      CosmereAPI.updateBook(id, data),
    onSuccess: (updatedBook: Book) => {
      // Update the book in cache
      queryClient.setQueryData(bookKeys.detail(updatedBook.id), updatedBook);
      // Invalidate book lists
      queryClient.invalidateQueries({ queryKey: bookKeys.lists() });
    },
  });
};

// Hook for deleting a book
export const useDeleteBook = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => CosmereAPI.deleteBook(id),
    onSuccess: (_: void, deletedId: string) => {
      // Remove book from cache
      queryClient.removeQueries({ queryKey: bookKeys.detail(deletedId) });
      // Invalidate book lists
      queryClient.invalidateQueries({ queryKey: bookKeys.lists() });
    },
  });
};

// Hook for searching books
export const useSearchBooks = (
  query: string,
  filters?: BookFilters,
  size: number = 20
) => {
  return useQuery({
    queryKey: ['books', 'search', query, filters, size],
    queryFn: () => CosmereAPI.searchBooks(query, filters, size),
    enabled: !!query && query.length >= 2,
    staleTime: 2 * 60 * 1000, // 2 minutes for search results
  });
}; 