import React, { useEffect, useState } from 'react';
import { fetchWorlds } from '../services/api';

type World = {
  id: string;
  name: string;
  system?: string;
  geography?: string;
  technology_level?: string;
};

const Worlds: React.FC = () => {
  const [worlds, setWorlds] = useState<World[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchWorlds()
      .then(setWorlds)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading worlds...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <main>
      <h1>Cosmere Worlds</h1>
      <div>
        <h2>Worlds</h2>
        <ul>
          {worlds.map((world) => (
            <li key={world.id}>
              <strong>{world.name}</strong>
              {world.system && <span> (Magic: {world.system})</span>}
              {world.technology_level && <span> - {world.technology_level}</span>}
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
};

export default Worlds;
