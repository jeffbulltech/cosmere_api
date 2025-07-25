import React from 'react';
import { Link } from 'react-router-dom';
import { World } from '../../types/cosmere';

interface WorldCardProps {
  world: World;
  className?: string;
}

const WorldCard: React.FC<WorldCardProps> = ({ world, className = '' }) => {
  return (
    <Link 
      to={`/worlds/${world.id}`}
      className={`block bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200 ${className}`}
    >
      <div className="p-6">
        {/* Header */}
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {world.name}
          </h3>
          {world.system && (
            <p className="text-sm text-gray-500">
              System: {world.system}
            </p>
          )}
        </div>

        {/* Details */}
        <div className="space-y-2">
          {world.technology_level && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Technology:</span>
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                {world.technology_level}
              </span>
            </div>
          )}

          {world.shard_id && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Shard:</span>
              <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs">
                {world.shard_id}
              </span>
            </div>
          )}

          {world.magic_systems && Object.keys(world.magic_systems).length > 0 && (
            <div className="flex items-start text-sm text-gray-600">
              <span className="font-medium mr-2">Magic Systems:</span>
              <div className="flex flex-wrap gap-1">
                {Object.keys(world.magic_systems).slice(0, 2).map((system, index) => (
                  <span 
                    key={index}
                    className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs"
                  >
                    {system}
                  </span>
                ))}
                {Object.keys(world.magic_systems).length > 2 && (
                  <span className="text-xs text-gray-500">
                    +{Object.keys(world.magic_systems).length - 2} more
                  </span>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Culture Notes */}
        {world.culture_notes && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <p className="text-sm text-gray-600 line-clamp-3">
              {world.culture_notes}
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
          <span className="text-gray-400">
            {new Date(world.created_at).toLocaleDateString()}
          </span>
          <div className="flex items-center space-x-2">
            <span>🌍</span>
            <span>View Details</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default WorldCard;
