import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Character } from '../types/cosmere';
import { fetchCharacter, deleteCharacter } from '../services/api';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorBoundary from '../components/common/ErrorBoundary';
import { parseCharacter, getStatusColor, getStatusDisplay } from '../utils/helpers';

const CharacterDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [character, setCharacter] = useState<Character | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const loadCharacter = async (characterId: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchCharacter(characterId);
      setCharacter(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load character');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!character) return;
    
    try {
      await deleteCharacter(character.id);
      navigate('/characters');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete character');
    }
  };

  useEffect(() => {
    if (id) {
      loadCharacter(id);
    }
  }, [id]);

  if (loading) {
    return <LoadingSpinner message="Loading character..." />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <p className="text-lg font-medium">Error loading character</p>
          <p className="text-sm text-gray-600">{error}</p>
        </div>
        <button
          onClick={() => id && loadCharacter(id)}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!character) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Character Not Found</h1>
        <p className="text-gray-600 mb-8">The character you're looking for doesn't exist.</p>
        <Link
          to="/characters"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Characters
        </Link>
      </div>
    );
  }

  const parsedCharacter = parseCharacter(character);

  return (
    <ErrorBoundary>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{character.name}</h1>
              {parsedCharacter.aliases && parsedCharacter.aliases.length > 0 && (
                <p className="text-lg text-gray-600">
                  Also known as: {parsedCharacter.aliases.join(', ')}
                </p>
              )}
            </div>
            <div className="flex space-x-2">
              <Link
                to={`/characters/${character.id}/edit`}
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
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Basic Information</h2>
              <dl className="grid grid-cols-1 gap-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Status</dt>
                  <dd className="mt-1">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(character.status)}`}>
                      {getStatusDisplay(character.status)}
                    </span>
                  </dd>
                </div>
                {character.species && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Species</dt>
                    <dd className="mt-1 text-sm text-gray-900">{character.species}</dd>
                  </div>
                )}
                {character.world_of_origin_id && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">World of Origin</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      <Link
                        to={`/worlds/${character.world_of_origin_id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {character.world_of_origin_id}
                      </Link>
                    </dd>
                  </div>
                )}
                {character.first_appearance_book_id && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">First Appearance</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      <Link
                        to={`/books/${character.first_appearance_book_id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {character.first_appearance_book_id}
                      </Link>
                    </dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Biography */}
            {character.biography && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Biography</h2>
                <div className="prose max-w-none">
                  <p className="text-gray-700 leading-relaxed">{character.biography}</p>
                </div>
              </div>
            )}

            {/* Magic Abilities */}
            {parsedCharacter.magic_abilities && Object.keys(parsedCharacter.magic_abilities).length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Magic Abilities</h2>
                <div className="space-y-3">
                  {Object.entries(parsedCharacter.magic_abilities).map(([ability, details]) => (
                    <div key={ability} className="border-l-4 border-yellow-400 pl-4">
                      <h3 className="font-medium text-gray-900">{ability}</h3>
                      {typeof details === 'string' && (
                        <p className="text-sm text-gray-600 mt-1">{details}</p>
                      )}
                      {typeof details === 'object' && details && (
                        <div className="text-sm text-gray-600 mt-1">
                          {Object.entries(details).map(([key, value]) => (
                            <div key={key}>
                              <span className="font-medium">{key}:</span> {String(value)}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Affiliations */}
            {parsedCharacter.affiliations && Object.keys(parsedCharacter.affiliations).length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Affiliations</h2>
                <div className="space-y-3">
                  {Object.entries(parsedCharacter.affiliations).map(([affiliation, details]) => (
                    <div key={affiliation} className="border-l-4 border-green-400 pl-4">
                      <h3 className="font-medium text-gray-900">{affiliation}</h3>
                      {typeof details === 'string' && (
                        <p className="text-sm text-gray-600 mt-1">{details}</p>
                      )}
                      {typeof details === 'object' && details && (
                        <div className="text-sm text-gray-600 mt-1">
                          {Object.entries(details).map(([key, value]) => (
                            <div key={key}>
                              <span className="font-medium">{key}:</span> {String(value)}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Cosmere Significance */}
            {parsedCharacter.cosmere_significance && Object.keys(parsedCharacter.cosmere_significance).length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Cosmere Significance</h2>
                <div className="space-y-3">
                  {Object.entries(parsedCharacter.cosmere_significance).map(([aspect, details]) => (
                    <div key={aspect} className="border-l-4 border-purple-400 pl-4">
                      <h3 className="font-medium text-gray-900">{aspect}</h3>
                      {typeof details === 'string' && (
                        <p className="text-sm text-gray-600 mt-1">{details}</p>
                      )}
                      {typeof details === 'object' && details && (
                        <div className="text-sm text-gray-600 mt-1">
                          {Object.entries(details).map(([key, value]) => (
                            <div key={key}>
                              <span className="font-medium">{key}:</span> {String(value)}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h2>
              <dl className="space-y-3">
                <div className="flex justify-between">
                  <dt className="text-sm text-gray-500">Books Appearances</dt>
                  <dd className="text-sm font-medium text-gray-900">{character.book_count || 0}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-sm text-gray-500">Relationships</dt>
                  <dd className="text-sm font-medium text-gray-900">{character.relationship_count || 0}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-sm text-gray-500">Magic Abilities</dt>
                  <dd className="text-sm font-medium text-gray-900">
                    {parsedCharacter.magic_abilities ? Object.keys(parsedCharacter.magic_abilities).length : 0}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-sm text-gray-500">Affiliations</dt>
                  <dd className="text-sm font-medium text-gray-900">
                    {parsedCharacter.affiliations ? Object.keys(parsedCharacter.affiliations).length : 0}
                  </dd>
                </div>
              </dl>
            </div>

            {/* Related Links */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Related Links</h2>
              <div className="space-y-2">
                <Link
                  to="/characters"
                  className="block text-sm text-blue-600 hover:text-blue-800"
                >
                  ← Back to Characters
                </Link>
                {character.world_of_origin_id && (
                  <Link
                    to={`/worlds/${character.world_of_origin_id}`}
                    className="block text-sm text-blue-600 hover:text-blue-800"
                  >
                    View World: {character.world_of_origin_id}
                  </Link>
                )}
                {character.first_appearance_book_id && (
                  <Link
                    to={`/books/${character.first_appearance_book_id}`}
                    className="block text-sm text-blue-600 hover:text-blue-800"
                  >
                    View First Appearance Book
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Delete Confirmation Modal */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3 text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Delete Character</h3>
                <p className="text-sm text-gray-500 mb-6">
                  Are you sure you want to delete "{character.name}"? This action cannot be undone.
                </p>
                <div className="flex justify-center space-x-3">
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleDelete}
                    className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
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

export default CharacterDetail; 