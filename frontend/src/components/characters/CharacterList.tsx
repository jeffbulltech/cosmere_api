import React, { useState, useEffect } from 'react';
import { Character, CharacterFilters } from '../../types/cosmere';
import { fetchCharacters } from '../../services/api';
import CharacterCard from './CharacterCard';
import LoadingSpinner from '../common/LoadingSpinner';
import SearchBar from '../common/SearchBar';

interface CharacterListProps {
  className?: string;
}

const CharacterList: React.FC<CharacterListProps> = ({ className = '' }) => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<CharacterFilters>({});
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrev, setHasPrev] = useState(false);

  const limit = 20;

  const loadCharacters = async (page: number = 1, newFilters?: CharacterFilters) => {
    try {
      setLoading(true);
      setError(null);
      
      const skip = (page - 1) * limit;
      const response = await fetchCharacters({
        ...filters,
        ...newFilters,
      });
      
      setCharacters(response.items);
      setTotal(response.total);
      setHasNext(response.has_next);
      setHasPrev(response.has_prev);
      setCurrentPage(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load characters');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCharacters(1);
  }, []);

  const handleSearch = (query: string) => {
    const newFilters = { ...filters, search: query };
    setFilters(newFilters);
    loadCharacters(1, newFilters);
  };

  const handleFilterChange = (key: keyof CharacterFilters, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    loadCharacters(1, newFilters);
  };

  const handlePageChange = (page: number) => {
    loadCharacters(page);
  };

  if (error) {
    return (
      <div className={`text-center py-8 ${className}`}>
        <div className="text-red-600 mb-4">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <p className="text-lg font-medium">Error loading characters</p>
          <p className="text-sm text-gray-600">{error}</p>
        </div>
        <button
          onClick={() => loadCharacters(1)}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className={className}>
      {/* Header and Filters */}
      <div className="mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Characters</h2>
            <p className="text-gray-600">Explore the characters of the Cosmere universe</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-500">
              {total} character{total !== 1 ? 's' : ''}
            </span>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="space-y-4">
          <SearchBar
            onSearch={handleSearch}
            placeholder="Search characters by name or aliases..."
            className="max-w-md"
          />
          
          <div className="flex flex-wrap gap-2">
            <select
              value={filters.status || ''}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Status</option>
              <option value="alive">Alive</option>
              <option value="dead">Dead</option>
              <option value="cognitive_shadow">Cognitive Shadow</option>
              <option value="unknown">Unknown</option>
            </select>

            <select
              value={filters.species || ''}
              onChange={(e) => handleFilterChange('species', e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Species</option>
              <option value="Human">Human</option>
              <option value="Koloss">Koloss</option>
              <option value="Kandra">Kandra</option>
              <option value="Parshendi">Parshendi</option>
              <option value="Spren">Spren</option>
            </select>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingSpinner message="Loading characters..." />
      )}

      {/* Character Grid */}
      {!loading && characters.length > 0 && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {characters.map((character) => (
              <CharacterCard key={character.id} character={character} />
            ))}
          </div>

          {/* Pagination */}
          {(hasNext || hasPrev) && (
            <div className="mt-8 flex items-center justify-center space-x-2">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={!hasPrev}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              
              <span className="px-4 py-2 text-sm text-gray-700">
                Page {currentPage} of {Math.ceil(total / limit)}
              </span>
              
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={!hasNext}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}

      {/* Empty State */}
      {!loading && characters.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No characters found</h3>
          <p className="text-gray-600">
            Try adjusting your search or filters to find what you're looking for.
          </p>
        </div>
      )}
    </div>
  );
};

export default CharacterList;
