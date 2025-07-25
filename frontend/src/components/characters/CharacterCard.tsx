import React from 'react';
import { Link } from 'react-router-dom';
import { Character } from '../../types/cosmere';
import { parseCharacter, getStatusColor, getStatusDisplay, truncateText } from '../../utils/helpers';

interface CharacterCardProps {
  character: Character;
  className?: string;
}

const CharacterCard: React.FC<CharacterCardProps> = ({ character, className = '' }) => {
  const parsedCharacter = parseCharacter(character);

  const getStatusIcon = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'alive':
        return '🟢';
      case 'dead':
        return '🔴';
      case 'cognitive_shadow':
        return '👻';
      default:
        return '❓';
    }
  };

  return (
    <Link 
      to={`/characters/${character.id}`}
      className={`block bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200 ${className}`}
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {character.name}
            </h3>
            {parsedCharacter.aliases && parsedCharacter.aliases.length > 0 && (
              <p className="text-sm text-gray-500 truncate">
                Also known as: {parsedCharacter.aliases.join(', ')}
              </p>
            )}
          </div>
          <div className={`ml-2 flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(character.status)}`}>
            <span className="mr-1">{getStatusIcon(character.status)}</span>
            {getStatusDisplay(character.status)}
          </div>
        </div>

        {/* Details */}
        <div className="space-y-2">
          {character.species && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Species:</span>
              <span>{character.species}</span>
            </div>
          )}

          {character.world_of_origin_id && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">World:</span>
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                {character.world_of_origin_id}
              </span>
            </div>
          )}

          {/* Magic abilities */}
          {parsedCharacter.magic_abilities && Object.keys(parsedCharacter.magic_abilities).length > 0 && (
            <div className="flex items-start text-sm text-gray-600">
              <span className="font-medium mr-2">Magic:</span>
              <div className="flex flex-wrap gap-1">
                {Object.keys(parsedCharacter.magic_abilities).slice(0, 3).map((ability, index) => (
                  <span 
                    key={index}
                    className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs"
                  >
                    {ability}
                  </span>
                ))}
                {Object.keys(parsedCharacter.magic_abilities).length > 3 && (
                  <span className="text-xs text-gray-500">
                    +{Object.keys(parsedCharacter.magic_abilities).length - 3} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Affiliations */}
          {parsedCharacter.affiliations && Object.keys(parsedCharacter.affiliations).length > 0 && (
            <div className="flex items-start text-sm text-gray-600">
              <span className="font-medium mr-2">Affiliations:</span>
              <div className="flex flex-wrap gap-1">
                {Object.keys(parsedCharacter.affiliations).slice(0, 2).map((affiliation, index) => (
                  <span 
                    key={index}
                    className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs"
                  >
                    {affiliation}
                  </span>
                ))}
                {Object.keys(parsedCharacter.affiliations).length > 2 && (
                  <span className="text-xs text-gray-500">
                    +{Object.keys(parsedCharacter.affiliations).length - 2} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Biography preview */}
          {character.biography && (
            <div className="text-sm text-gray-600">
              <span className="font-medium mr-2">Bio:</span>
              <span>{truncateText(character.biography, 80)}</span>
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center space-x-4">
            <span>📚 {character.book_count || 0} books</span>
            <span>👥 {character.relationship_count || 0} relationships</span>
          </div>
          <span className="text-gray-400">
            {new Date(character.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>
    </Link>
  );
};

export default CharacterCard;
