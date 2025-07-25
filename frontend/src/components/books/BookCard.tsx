import React from 'react';
import { Link } from 'react-router-dom';
import { Book } from '../../types/cosmere';

interface BookCardProps {
  book: Book;
  className?: string;
}

const BookCard: React.FC<BookCardProps> = ({ book, className = '' }) => {
  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Unknown';
    return new Date(dateString).getFullYear();
  };

  return (
    <Link 
      to={`/books/${book.id}`}
      className={`block bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200 ${className}`}
    >
      <div className="p-6">
        {/* Header */}
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900 line-clamp-2 mb-2">
            {book.title}
          </h3>
          {book.publication_date && (
            <p className="text-sm text-gray-500">
              Published: {formatDate(book.publication_date)}
            </p>
          )}
        </div>

        {/* Details */}
        <div className="space-y-2">
          {book.world_id && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">World:</span>
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                {book.world_id}
              </span>
            </div>
          )}

          {book.series_id && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Series:</span>
              <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                {book.series_id}
              </span>
            </div>
          )}

          {book.chronological_order && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Chronological Order:</span>
              <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs">
                #{book.chronological_order}
              </span>
            </div>
          )}

          {book.word_count && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Word Count:</span>
              <span>{book.word_count.toLocaleString()}</span>
            </div>
          )}

          {book.isbn && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">ISBN:</span>
              <span className="font-mono text-xs">{book.isbn}</span>
            </div>
          )}
        </div>

        {/* Summary */}
        {book.summary && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <p className="text-sm text-gray-600 line-clamp-3">
              {book.summary}
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
          <span className="text-gray-400">
            {new Date(book.created_at).toLocaleDateString()}
          </span>
          <div className="flex items-center space-x-2">
            <span>📚</span>
            <span>View Details</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default BookCard;
