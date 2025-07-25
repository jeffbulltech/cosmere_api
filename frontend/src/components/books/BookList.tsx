import React, { useState, useEffect } from 'react';
import { Book, BookFilters } from '../../types/cosmere';
import { fetchBooks } from '../../services/api';
import BookCard from './BookCard';
import LoadingSpinner from '../common/LoadingSpinner';
import SearchBar from '../common/SearchBar';

interface BookListProps {
  className?: string;
}

const BookList: React.FC<BookListProps> = ({ className = '' }) => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<BookFilters>({});
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrev, setHasPrev] = useState(false);

  const limit = 20;

  const loadBooks = async (page: number = 1, newFilters?: BookFilters) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetchBooks({
        ...filters,
        ...newFilters,
      });
      
      setBooks(response.items);
      setTotal(response.total);
      setHasNext(response.has_next);
      setHasPrev(response.has_prev);
      setCurrentPage(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load books');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBooks(1);
  }, []);

  const handleSearch = (query: string) => {
    const newFilters = { ...filters, search: query };
    setFilters(newFilters);
    loadBooks(1, newFilters);
  };

  const handleFilterChange = (key: keyof BookFilters, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    loadBooks(1, newFilters);
  };

  const handlePageChange = (page: number) => {
    loadBooks(page);
  };

  if (error) {
    return (
      <div className={`text-center py-8 ${className}`}>
        <div className="text-red-600 mb-4">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <p className="text-lg font-medium">Error loading books</p>
          <p className="text-sm text-gray-600">{error}</p>
        </div>
        <button
          onClick={() => loadBooks(1)}
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
            <h2 className="text-2xl font-bold text-gray-900">Books</h2>
            <p className="text-gray-600">Explore the books of the Cosmere universe</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-500">
              {total} book{total !== 1 ? 's' : ''}
            </span>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="space-y-4">
          <SearchBar
            onSearch={handleSearch}
            placeholder="Search books by title..."
            className="max-w-md"
          />
          
          <div className="flex flex-wrap gap-2">
            <input
              type="number"
              placeholder="Publication Year"
              value={filters.publication_year || ''}
              onChange={(e) => handleFilterChange('publication_year', e.target.value ? parseInt(e.target.value).toString() : '')}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingSpinner message="Loading books..." />
      )}

      {/* Book Grid */}
      {!loading && books.length > 0 && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {books.map((book) => (
              <BookCard key={book.id} book={book} />
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
      {!loading && books.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No books found</h3>
          <p className="text-gray-600">
            Try adjusting your search or filters to find what you're looking for.
          </p>
        </div>
      )}
    </div>
  );
};

export default BookList;
