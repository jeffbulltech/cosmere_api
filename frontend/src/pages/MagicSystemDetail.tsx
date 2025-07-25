import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { fetchMagicSystem, deleteMagicSystem } from '../services/api';
import { MagicSystem } from '../types/cosmere';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorBoundary from '../components/common/ErrorBoundary';

const MagicSystemDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [magicSystem, setMagicSystem] = useState<MagicSystem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    if (id) {
      loadMagicSystem(id);
    }
  }, [id]);

  const loadMagicSystem = async (magicSystemId: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchMagicSystem(magicSystemId);
      setMagicSystem(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load magic system');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!magicSystem) return;
    
    try {
      await deleteMagicSystem(magicSystem.id);
      navigate('/magic-systems');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete magic system');
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
          to="/magic-systems"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Magic Systems
        </Link>
      </div>
    );
  }

  if (!magicSystem) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Magic System Not Found</h2>
        <Link
          to="/magic-systems"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Magic Systems
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
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{magicSystem.name}</h1>
              <p className="text-lg text-gray-600">
                Type: {magicSystem.type}
              </p>
            </div>
            <div className="flex space-x-2">
              <Link
                to={`/magic-systems/${magicSystem.id}/edit`}
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
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Magic System Information</h2>
              <dl className="grid grid-cols-1 gap-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Type</dt>
                  <dd className="mt-1 text-sm text-gray-900">{magicSystem.type}</dd>
                </div>
                {magicSystem.power_source && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Power Source</dt>
                    <dd className="mt-1 text-sm text-gray-900">{magicSystem.power_source}</dd>
                  </div>
                )}
                {magicSystem.world_id && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">World</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      <Link
                        to={`/worlds/${magicSystem.world_id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {magicSystem.world_id}
                      </Link>
                    </dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Description */}
            {magicSystem.description && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Description</h2>
                <div className="prose max-w-none">
                  <p className="text-gray-700 leading-relaxed">{magicSystem.description}</p>
                </div>
              </div>
            )}

            {/* Mechanics */}
            {magicSystem.has_mechanics && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Mechanics</h2>
                {magicSystem.mechanics_list && magicSystem.mechanics_list.length > 0 ? (
                  <div className="space-y-2">
                    {magicSystem.mechanics_list.map((mechanic, index) => (
                      <div key={index} className="flex items-center">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {mechanic}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No specific mechanics listed.</p>
                )}
              </div>
            )}

            {/* Limitations */}
            {magicSystem.has_limitations && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Limitations</h2>
                {magicSystem.limitations_list && magicSystem.limitations_list.length > 0 ? (
                  <div className="space-y-2">
                    {magicSystem.limitations_list.map((limitation, index) => (
                      <div key={index} className="flex items-center">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                          {limitation}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No specific limitations listed.</p>
                )}
              </div>
            )}

            {/* Raw Data */}
            {(magicSystem.mechanics && Object.keys(magicSystem.mechanics).length > 0) && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Mechanics (Raw Data)</h2>
                <div className="prose max-w-none">
                  <pre className="text-sm text-gray-700 bg-gray-50 p-4 rounded overflow-x-auto">
                    {JSON.stringify(magicSystem.mechanics, null, 2)}
                  </pre>
                </div>
              </div>
            )}

            {(magicSystem.limitations && Object.keys(magicSystem.limitations).length > 0) && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Limitations (Raw Data)</h2>
                <div className="prose max-w-none">
                  <pre className="text-sm text-gray-700 bg-gray-50 p-4 rounded overflow-x-auto">
                    {JSON.stringify(magicSystem.limitations, null, 2)}
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
                {magicSystem.world_id && (
                  <Link
                    to={`/worlds/${magicSystem.world_id}`}
                    className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                  >
                    View World
                  </Link>
                )}
                <Link
                  to={`/magic-systems/${magicSystem.id}/characters`}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  View Users
                </Link>
              </div>
            </div>

            {/* Magic System Details */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Magic System Details</h2>
              <dl className="space-y-3">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Category</dt>
                  <dd className="text-sm text-gray-900">{magicSystem.type}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Has Mechanics</dt>
                  <dd className="text-sm text-gray-900">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      magicSystem.has_mechanics ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {magicSystem.has_mechanics ? 'Yes' : 'No'}
                    </span>
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Has Limitations</dt>
                  <dd className="text-sm text-gray-900">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      magicSystem.has_limitations ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {magicSystem.has_limitations ? 'Yes' : 'No'}
                    </span>
                  </dd>
                </div>
                {magicSystem.power_source && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Power Source</dt>
                    <dd className="text-sm text-gray-900">{magicSystem.power_source}</dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Metadata */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Metadata</h2>
              <dl className="space-y-2 text-sm">
                <div>
                  <dt className="font-medium text-gray-500">Created</dt>
                  <dd className="text-gray-900">{new Date(magicSystem.created_at).toLocaleDateString()}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Last Updated</dt>
                  <dd className="text-gray-900">{new Date(magicSystem.updated_at).toLocaleDateString()}</dd>
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
                <h3 className="text-lg font-medium text-gray-900 mb-4">Delete Magic System</h3>
                <p className="text-sm text-gray-500 mb-6">
                  Are you sure you want to delete "{magicSystem.name}"? This action cannot be undone.
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

export default MagicSystemDetail; 