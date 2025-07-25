import React, { useState, useEffect } from 'react';
import { MagicSystem, MagicSystemFilters } from '../../types/cosmere';
import { fetchMagicSystems } from '../../services/api';
import MagicSystemCard from './MagicSystemCard';
import LoadingSpinner from '../common/LoadingSpinner';
import SearchBar from '../common/SearchBar';

interface MagicSystemListProps {
  className?: string;
}

const MagicSystemList: React.FC<MagicSystemListProps> = ({ className = '' }) => {
  const [magicSystems, setMagicSystems] = useState<MagicSystem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<MagicSystemFilters>({});
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrev, setHasPrev] = useState(false);

  const limit = 20;

  const loadMagicSystems = async (page: number = 1, newFilters?: MagicSystemFilters) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetchMagicSystems({
        ...filters,
        ...newFilters,
      });
      
      setMagicSystems(response.items);
      setTotal(response.total);
      setHasNext(response.has_next);
      setHasPrev(response.has_prev);
      setCurrentPage(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load magic systems');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMagicSystems(1);
  }, []);

  const handleSearch = (query: string) => {
    const newFilters = { ...filters, search: query };
    setFilters(newFilters);
    loadMagicSystems(1, newFilters);
  };

  const handleFilterChange = (key: keyof MagicSystemFilters, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    loadMagicSystems(1, newFilters);
  };

  const handlePageChange = (page: number) => {
    loadMagicSystems(page);
  };

  if (error) {
    return (
      <div className={`text-center py-8 ${className}`}>
        <div className="text-red-600 mb-4">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <p className="text-lg font-medium">Error loading magic systems</p>
          <p className="text-sm text-gray-600">{error}</p>
        </div>
        <button
          onClick={() => loadMagicSystems(1)}
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
            <h2 className="text-2xl font-bold text-gray-900">Magic Systems</h2>
            <p className="text-gray-600">Discover the unique magic systems of the Cosmere universe</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-500">
              {total} magic system{total !== 1 ? 's' : ''}
            </span>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="space-y-4">
          <SearchBar
            onSearch={handleSearch}
            placeholder="Search magic systems by name..."
            className="max-w-md"
          />
          
          <div className="flex flex-wrap gap-2">
            <select
              value={filters.type || ''}
              onChange={(e) => handleFilterChange('type', e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="allomancy">Allomancy</option>
              <option value="feruchemy">Feruchemy</option>
              <option value="hemalurgy">Hemalurgy</option>
              <option value="surgebinding">Surgebinding</option>
              <option value="awakening">Awakening</option>
              <option value="forging">Forging</option>
              <option value="aether">Aether</option>
            </select>

            <select
              value={filters.power_source || ''}
              onChange={(e) => handleFilterChange('power_source', e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Power Sources</option>
              <option value="preservation">Preservation</option>
              <option value="ruin">Ruin</option>
              <option value="honor">Honor</option>
              <option value="cultivation">Cultivation</option>
              <option value="endowment">Endowment</option>
              <option value="autonomy">Autonomy</option>
            </select>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingSpinner message="Loading magic systems..." />
      )}

      {/* Magic System Grid */}
      {!loading && magicSystems.length > 0 && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {magicSystems.map((magicSystem) => (
              <MagicSystemCard key={magicSystem.id} magicSystem={magicSystem} />
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
      {!loading && magicSystems.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0h10m-10 0a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2M9 12l2 2 4-4" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No magic systems found</h3>
          <p className="text-gray-600">
            Try adjusting your search or filters to find what you're looking for.
          </p>
        </div>
      )}
    </div>
  );
};

export default MagicSystemList; 