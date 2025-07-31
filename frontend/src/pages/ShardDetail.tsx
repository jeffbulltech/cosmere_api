import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { fetchShard, deleteShard } from '../services/api';
import { Shard } from '../types/cosmere';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorBoundary from '../components/common/ErrorBoundary';

const ShardDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [shard, setShard] = useState<Shard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    if (id) {
      loadShard(id);
    }
  }, [id]);

  const loadShard = async (shardId: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchShard(shardId);
      setShard(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load shard');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!shard) return;
    
    try {
      await deleteShard(shard.id);
      navigate('/shards');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete shard');
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
          to="/shards"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Shards
        </Link>
      </div>
    );
  }

  if (!shard) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Shard Not Found</h2>
        <Link
          to="/shards"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Back to Shards
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
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{shard.name}</h1>
              <p className="text-lg text-gray-600">
                Intent: {shard.intent}
              </p>
            </div>
            <div className="flex space-x-2">
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
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Shard Information</h2>
              <dl className="grid grid-cols-1 gap-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Intent</dt>
                  <dd className="mt-1 text-sm text-gray-900">{shard.intent}</dd>
                </div>
                {shard.vessel_name && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Vessel</dt>
                    <dd className="mt-1 text-sm text-gray-900">{shard.vessel_name}</dd>
                  </div>
                )}
                {shard.vessel_status && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Vessel Status</dt>
                    <dd className="mt-1 text-sm text-gray-900">{shard.vessel_status}</dd>
                  </div>
                )}
                {shard.world_location_id && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">World Location</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      <Link
                        to={`/worlds/${shard.world_location_id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {shard.world_location_id}
                      </Link>
                    </dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Description */}
            {shard.description && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Description</h2>
                <div className="prose max-w-none">
                  <p className="text-gray-700 leading-relaxed">{shard.description}</p>
                </div>
              </div>
            )}

            {/* Splinter Information */}
            {shard.splinter_info && Object.keys(shard.splinter_info).length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Splinter Information</h2>
                <div className="prose max-w-none">
                  <pre className="text-sm text-gray-700 bg-gray-50 p-4 rounded overflow-x-auto">
                    {JSON.stringify(shard.splinter_info, null, 2)}
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
                  to={`/shards/${shard.id}/worlds`}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                >
                  View Worlds
                </Link>
                {shard.world_location_id && (
                  <Link
                    to={`/worlds/${shard.world_location_id}`}
                    className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    View World Location
                  </Link>
                )}
              </div>
            </div>

            {/* Shard Details */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Shard Details</h2>
              <dl className="space-y-3">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Type</dt>
                  <dd className="text-sm text-gray-900">Cosmere Shard</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Status</dt>
                  <dd className="text-sm text-gray-900">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      shard.vessel_status === 'alive' ? 'bg-green-100 text-green-800' :
                      shard.vessel_status === 'dead' ? 'bg-red-100 text-red-800' :
                      shard.vessel_status === 'splintered' ? 'bg-purple-100 text-purple-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {shard.vessel_status?.toUpperCase() || 'Unknown'}
                    </span>
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Has Vessel</dt>
                  <dd className="text-sm text-gray-900">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      shard.vessel_name ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {shard.vessel_name ? 'Yes' : 'No'}
                    </span>
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Has World Location</dt>
                  <dd className="text-sm text-gray-900">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      shard.world_location_id ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {shard.world_location_id ? 'Yes' : 'No'}
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
                  <dd className="text-gray-900">{new Date(shard.created_at).toLocaleDateString()}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Last Updated</dt>
                  <dd className="text-gray-900">{new Date(shard.updated_at).toLocaleDateString()}</dd>
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
                <h3 className="text-lg font-medium text-gray-900 mb-4">Delete Shard</h3>
                <p className="text-sm text-gray-500 mb-6">
                  Are you sure you want to delete "{shard.name}"? This action cannot be undone.
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

export default ShardDetail; 