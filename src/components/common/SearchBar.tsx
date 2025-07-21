import React, { useState, useRef, useEffect } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useQuery } from '@tanstack/react-query';
import CosmereAPI from '../../services/api';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  className?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  onSearch, 
  placeholder = "Search characters, books, worlds...",
  className = ""
}) => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const searchRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Search query with debouncing
  const { data: searchResults, isLoading } = useQuery({
    queryKey: ['global-search', query],
    queryFn: () => CosmereAPI.globalSearch(query),
    enabled: query.length >= 2,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!searchResults?.items) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < searchResults.items.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && searchResults.items[selectedIndex]) {
          handleResultClick(searchResults.items[selectedIndex]);
        } else if (query.trim()) {
          onSearch(query);
          setIsOpen(false);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setSelectedIndex(-1);
        break;
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setIsOpen(value.length >= 2);
    setSelectedIndex(-1);
  };

  const handleResultClick = (result: any) => {
    // Navigate based on result type
    const type = result.type || 'unknown';
    const id = result.id;
    
    switch (type) {
      case 'character':
        window.location.href = `/characters/${id}`;
        break;
      case 'book':
        window.location.href = `/books/${id}`;
        break;
      case 'world':
        window.location.href = `/worlds/${id}`;
        break;
      default:
        onSearch(query);
    }
    
    setIsOpen(false);
    setQuery('');
  };

  const getResultIcon = (type: string) => {
    switch (type) {
      case 'character':
        return '👤';
      case 'book':
        return '📚';
      case 'world':
        return '🌍';
      case 'magic_system':
        return '✨';
      default:
        return '🔍';
    }
  };

  return (
    <div ref={searchRef} className={`relative ${className}`}>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
        </div>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
          placeholder={placeholder}
          className="input-field pl-10 pr-4 py-2 w-full"
        />
        {isLoading && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            <div className="spinner w-4 h-4"></div>
          </div>
        )}
      </div>

      {/* Search Results Dropdown */}
      {isOpen && searchResults && (
        <div className="absolute z-50 w-full mt-1 bg-white rounded-md shadow-lg border border-gray-200 max-h-96 overflow-y-auto">
          {searchResults.items.length > 0 ? (
            <ul className="py-1">
              {searchResults.items.map((result: any, index: number) => (
                <li
                  key={`${result.type}-${result.id}`}
                  className={`px-4 py-2 cursor-pointer hover:bg-gray-50 flex items-center space-x-3 ${
                    index === selectedIndex ? 'bg-cosmere-50' : ''
                  }`}
                  onClick={() => handleResultClick(result)}
                >
                  <span className="text-lg">{getResultIcon(result.type)}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {result.name || result.title}
                    </p>
                    <p className="text-xs text-gray-500 capitalize">
                      {result.type?.replace('_', ' ')} • {result.world_name || 'Unknown World'}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="px-4 py-3 text-sm text-gray-500">
              No results found for "{query}"
            </div>
          )}
          
          {searchResults.items.length > 0 && (
            <div className="border-t border-gray-200 px-4 py-2">
              <button
                onClick={() => {
                  onSearch(query);
                  setIsOpen(false);
                }}
                className="text-sm text-cosmere-600 hover:text-cosmere-800 font-medium"
              >
                View all results for "{query}"
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar; 