import React from 'react';
import CharacterList from '../components/characters/CharacterList';

const Characters: React.FC = () => {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Cosmere Characters</h1>
        <p className="text-gray-600">
          Discover the rich cast of characters that populate Brandon Sanderson's Cosmere universe. 
          From worldhoppers to local heroes, explore their stories, abilities, and connections.
        </p>
      </div>
      
      <CharacterList />
    </div>
  );
};

export default Characters;
