import React from 'react';
import { Link } from 'react-router-dom';
import { MagicSystem } from '../../types/cosmere';
import { parseMagicSystem, truncateText } from '../../utils/helpers';

interface MagicSystemCardProps {
  magicSystem: MagicSystem;
  className?: string;
}

const MagicSystemCard: React.FC<MagicSystemCardProps> = ({ magicSystem, className = '' }) => {
  const parsedMagicSystem = parseMagicSystem(magicSystem);

  return (
    <Link 
      to={`/magic-systems/${magicSystem.id}`}
      className={`block bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200 ${className}`}
    >
      <div className="p-6">
        {/* Header */}
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {magicSystem.name}
          </h3>
          <div className="flex items-center space-x-2">
            <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs font-medium">
              {magicSystem.type}
            </span>
            {magicSystem.world_id && (
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                {magicSystem.world_id}
              </span>
            )}
          </div>
        </div>

        {/* Details */}
        <div className="space-y-2">
          {magicSystem.power_source && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Power Source:</span>
              <span>{magicSystem.power_source}</span>
            </div>
          )}

          {/* Mechanics */}
          {parsedMagicSystem.mechanics && Object.keys(parsedMagicSystem.mechanics).length > 0 && (
            <div className="flex items-start text-sm text-gray-600">
              <span className="font-medium mr-2">Mechanics:</span>
              <div className="flex flex-wrap gap-1">
                {Object.keys(parsedMagicSystem.mechanics).slice(0, 2).map((mechanic, index) => (
                  <span 
                    key={index}
                    className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs"
                  >
                    {mechanic}
                  </span>
                ))}
                {Object.keys(parsedMagicSystem.mechanics).length > 2 && (
                  <span className="text-xs text-gray-500">
                    +{Object.keys(parsedMagicSystem.mechanics).length - 2} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Limitations */}
          {parsedMagicSystem.limitations && Object.keys(parsedMagicSystem.limitations).length > 0 && (
            <div className="flex items-start text-sm text-gray-600">
              <span className="font-medium mr-2">Limitations:</span>
              <div className="flex flex-wrap gap-1">
                {Object.keys(parsedMagicSystem.limitations).slice(0, 2).map((limitation, index) => (
                  <span 
                    key={index}
                    className="bg-red-100 text-red-800 px-2 py-1 rounded text-xs"
                  >
                    {limitation}
                  </span>
                ))}
                {Object.keys(parsedMagicSystem.limitations).length > 2 && (
                  <span className="text-xs text-gray-500">
                    +{Object.keys(parsedMagicSystem.limitations).length - 2} more
                  </span>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Description */}
        {magicSystem.description && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <p className="text-sm text-gray-600 line-clamp-3">
              {truncateText(magicSystem.description, 120)}
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
          <span className="text-gray-400">
            {new Date(magicSystem.created_at).toLocaleDateString()}
          </span>
          <div className="flex items-center space-x-2">
            <span>✨</span>
            <span>View Details</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default MagicSystemCard; 