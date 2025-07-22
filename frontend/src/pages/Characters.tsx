import React, { useEffect, useState } from 'react';
import { fetchCharacters } from '../services/api';

type Character = {
  id: string;
  name: string;
  world_of_origin_id?: string;
  species?: string;
  status?: string;
};

const Characters: React.FC = () => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCharacters()
      .then(setCharacters)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading characters...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <main>
      <h1>Cosmere Characters</h1>
      <div>
        <h2>Characters</h2>
        <ul>
          {characters.map((character) => (
            <li key={character.id}>
              <strong>{character.name}</strong>
              {character.world_of_origin_id && <span> (World: {character.world_of_origin_id})</span>}
              {character.species && <span> - {character.species}</span>}
              {character.status && <span> - {character.status}</span>}
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
};

export default Characters;
