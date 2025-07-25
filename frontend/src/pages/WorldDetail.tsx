import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { fetchWorld, deleteWorld } from '../services/api';
import { World } from '../types/cosmere';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorBoundary from '../components/common/ErrorBoundary';

const WorldDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [world, setWorld] = useState<World | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    if (id) {
      loadWorld(id);
    }
  }, [id]);

  const loadWorld = async (worldId: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchWorld(worldId);
      setWorld(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load world');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!world) return;
    
    try {
      await deleteWorld(world.id);
      navigate('/worlds');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete world');
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
          to="/worlds"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Worlds
        </Link>
      </div>
    );
  }

  if (!world) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">World Not Found</h2>
        <Link
          to="/worlds"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Worlds
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
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{world.name}</h1>
              {world.system && (
                <p className="text-lg text-gray-600">
                  System: {world.system}
                </p>
              )}
            </div>
            <div className="flex space-x-2">
              <Link
                to={`/worlds/${world.id}/edit`}
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
              <h2 className="text-xl font-semibold text-gray-900 mb-4">World Information</h2>
              <dl className="grid grid-cols-1 gap-4">
                {world.system && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">System</dt>
                    <dd className="mt-1 text-sm text-gray-900">{world.system}</dd>
                  </div>
                )}
                {world.technology_level && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Technology Level</dt>
                    <dd className="mt-1 text-sm text-gray-900">{world.technology_level}</dd>
                  </div>
                )}
                {world.shard_id && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Shard</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      <Link
                        to={`/shards/${world.shard_id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {world.shard_id}
                      </Link>
                    </dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Geography */}
            {world.geography && Object.keys(world.geography).length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Geography</h2>
                <div className="prose max-w-none">
                  <pre className="text-sm text-gray-700 bg-gray-50 p-4 rounded overflow-x-auto">
                    {JSON.stringify(world.geography, null, 2)}
                  </pre>
                </div>
              </div>
            )}

            {/* Culture Notes */}
            {world.culture_notes && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Culture</h2>
                <div className="prose max-w-none">
                  <p className="text-gray-700 leading-relaxed">{world.culture_notes}</p>
                </div>
              </div>
            )}

            {/* Magic Systems */}
            {world.magic_systems && Object.keys(world.magic_systems).length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Magic Systems</h2>
                <div className="prose max-w-none">
                  <pre className="text-sm text-gray-700 bg-gray-50 p-4 rounded overflow-x-auto">
                    {JSON.stringify(world.magic_systems, null, 2)}
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
                  to={`/worlds/${world.id}/characters`}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                >
                  View Characters
                </Link>
                <Link
                  to={`/worlds/${world.id}/books`}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  View Books
                </Link>
                <Link
                  to={`/worlds/${world.id}/magic-systems`}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  View Magic Systems
                </Link>
                {world.shard_id && (
                  <Link
                    to={`/shards/${world.shard_id}`}
                    className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    View Shard
                  </Link>
                )}
              </div>
            </div>

            {/* World Details */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">World Details</h2>
              <dl className="space-y-3">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Type</dt>
                  <dd className="text-sm text-gray-900">
                    {world.shard_id ? 'Shardworld' : 'Minor World'}
                  </dd>
                </div>
                {world.technology_level && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Development</dt>
                    <dd className="text-sm text-gray-900">{world.technology_level}</dd>
                  </div>
                )}
                <div>
                  <dt className="text-sm font-medium text-gray-500">Has Magic</dt>
                  <dd className="text-sm text-gray-900">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      world.magic_systems && Object.keys(world.magic_systems).length > 0 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {world.magic_systems && Object.keys(world.magic_systems).length > 0 ? 'Yes' : 'No'}
                    </span>
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
                  <dd className="text-gray-900">{new Date(world.created_at).toLocaleDateString()}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Last Updated</dt>
                  <dd className="text-gray-900">{new Date(world.updated_at).toLocaleDateString()}</dd>
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
                <h3 className="text-lg font-medium text-gray-900 mb-4">Delete World</h3>
                <p className="text-sm text-gray-500 mb-6">
                  Are you sure you want to delete "{world.name}"? This action cannot be undone.
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

export default WorldDetail; 