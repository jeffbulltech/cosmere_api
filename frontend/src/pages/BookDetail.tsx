import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { fetchBook, deleteBook } from '../services/api';
import { Book } from '../types/cosmere';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorBoundary from '../components/common/ErrorBoundary';

const BookDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    if (id) {
      loadBook(id);
    }
  }, [id]);

  const loadBook = async (bookId: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchBook(bookId);
      setBook(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load book');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!book) return;
    
    try {
      await deleteBook(book.id);
      navigate('/books');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete book');
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
        <p className="text-gray-600 mb-4">{error}</p>
        <Link
          to="/books"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Books
        </Link>
      </div>
    );
  }

  if (!book) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Book Not Found</h2>
        <Link
          to="/books"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Books
        </Link>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{book.title}</h1>
              {book.series_id && (
                <p className="text-lg text-gray-600">
                  Part of series: {book.series_id}
                </p>
              )}
            </div>
            <div className="flex space-x-2">
              <Link
                to={`/books/${book.id}/edit`}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Edit
              </Link>
              <button
                onClick={() => setShowDeleteConfirm(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Basic Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Book Information</h2>
              <dl className="grid grid-cols-1 gap-4">
                {book.publication_date && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Publication Date</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {new Date(book.publication_date).toLocaleDateString()}
                    </dd>
                  </div>
                )}
                {book.chronological_order && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Chronological Order</dt>
                    <dd className="mt-1 text-sm text-gray-900">{book.chronological_order}</dd>
                  </div>
                )}
                {book.word_count && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Word Count</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {book.word_count.toLocaleString()} words
                    </dd>
                  </div>
                )}
                {book.isbn && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">ISBN</dt>
                    <dd className="mt-1 text-sm text-gray-900">{book.isbn}</dd>
                  </div>
                )}
                {book.world_id && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">World</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      <Link
                        to={`/worlds/${book.world_id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {book.world_id}
                      </Link>
                    </dd>
                  </div>
                )}
                {book.series_id && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Series</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      <Link
                        to={`/series/${book.series_id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {book.series_id}
                      </Link>
                    </dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Summary */}
            {book.summary && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Summary</h2>
                <div className="prose max-w-none">
                  <p className="text-gray-700 leading-relaxed">{book.summary}</p>
                </div>
              </div>
            )}

            {/* Cosmere Significance */}
            {book.cosmere_significance && Object.keys(book.cosmere_significance).length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Cosmere Significance</h2>
                <div className="prose max-w-none">
                  <pre className="text-sm text-gray-700 bg-gray-50 p-4 rounded overflow-x-auto">
                    {JSON.stringify(book.cosmere_significance, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Stats & Actions */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
              <div className="space-y-3">
                <Link
                  to={`/books/${book.id}/characters`}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                >
                  View Characters
                </Link>
                <Link
                  to={`/books/${book.id}/world`}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  View World
                </Link>
                {book.series_id && (
                  <Link
                    to={`/series/${book.series_id}`}
                    className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    View Series
                  </Link>
                )}
              </div>
            </div>

            {/* Book Details */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Book Details</h2>
              <dl className="space-y-3">
                {book.word_count && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Length</dt>
                    <dd className="text-sm text-gray-900">
                      {book.word_count > 100000 ? 'Epic' : 
                       book.word_count > 80000 ? 'Long' : 
                       book.word_count > 60000 ? 'Standard' : 'Short'}
                    </dd>
                  </div>
                )}
                {book.publication_date && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Published</dt>
                    <dd className="text-sm text-gray-900">
                      {new Date(book.publication_date).getFullYear()}
                    </dd>
                  </div>
                )}
                <div>
                  <dt className="text-sm font-medium text-gray-500">Type</dt>
                  <dd className="text-sm text-gray-900">
                    {book.series_id ? 'Series Book' : 'Standalone'}
                  </dd>
                </div>
              </dl>
            </div>

            {/* Metadata */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Metadata</h2>
              <dl className="space-y-2 text-sm">
                <div>
                  <dt className="font-medium text-gray-500">Created</dt>
                  <dd className="text-gray-900">{new Date(book.created_at).toLocaleDateString()}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Last Updated</dt>
                  <dd className="text-gray-900">{new Date(book.updated_at).toLocaleDateString()}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        {/* Delete Confirmation Modal */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3 text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Delete Book</h3>
                <p className="text-sm text-gray-500 mb-6">
                  Are you sure you want to delete "{book.title}"? This action cannot be undone.
                </p>
                <div className="flex justify-center space-x-3">
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleDelete}
                    className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </ErrorBoundary>
  );
};

export default BookDetail; 