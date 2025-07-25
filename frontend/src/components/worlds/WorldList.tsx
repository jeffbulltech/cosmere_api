import React, { useState, useEffect } from 'react';
import { World } from '../../types/cosmere';
import { fetchWorlds } from '../../services/api';
import WorldCard from './WorldCard';
import LoadingSpinner from '../common/LoadingSpinner';
import SearchBar from '../common/SearchBar';

interface WorldListProps {
  className?: string;
}

const WorldList: React.FC<WorldListProps> = ({ className = '' }) => {
  const [worlds, setWorlds] = useState<World[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [total, setTotal] = useState(0);

  const loadWorlds = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetchWorlds();
      
      setWorlds(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load worlds');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorlds();
  }, []);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const filteredWorlds = worlds.filter(world =>
    world.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (world.system && world.system.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  if (error) {
    return (
      <div className={`text-center py-8 ${className}`}>
        <div className="text-red-600 mb-4">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <p className="text-lg font-medium">Error loading worlds</p>
          <p className="text-sm text-gray-600">{error}</p>
        </div>
        <button
          onClick={() => loadWorlds()}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className={className}>
      {/* Header and Search */}
      <div className="mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Worlds</h2>
            <p className="text-gray-600">Explore the diverse worlds of the Cosmere universe</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-500">
              {filteredWorlds.length} of {total} world{total !== 1 ? 's' : ''}
            </span>
          </div>
        </div>

        {/* Search */}
        <div className="space-y-4">
          <SearchBar
            onSearch={handleSearch}
            placeholder="Search worlds by name or system..."
            className="max-w-md"
          />
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingSpinner message="Loading worlds..." />
      )}

      {/* World Grid */}
      {!loading && filteredWorlds.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredWorlds.map((world) => (
            <WorldCard key={world.id} world={world} />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && filteredWorlds.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No worlds found</h3>
          <p className="text-gray-600">
            {searchQuery ? 'Try adjusting your search to find what you\'re looking for.' : 'No worlds are currently available.'}
          </p>
        </div>
      )}
    </div>
  );
};

export default WorldList;
