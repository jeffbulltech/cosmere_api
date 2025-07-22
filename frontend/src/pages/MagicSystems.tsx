import React, { useEffect, useState } from 'react';

type MagicSystem = {
  id: string;
  name: string;
  world_id?: string;
  type?: string;
  description?: string;
};

const MagicSystems: React.FC = () => {
  const [magicSystems, setMagicSystems] = useState<MagicSystem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // For now, we'll add a basic fetch function
    fetch('/api/v1/magic-systems/')
      .then(res => res.json())
      .then(data => setMagicSystems(data.items || data))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading magic systems...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <main>
      <h1>Cosmere Magic Systems</h1>
      <div>
        <h2>Magic Systems</h2>
        <ul>
          {magicSystems.map((magic) => (
            <li key={magic.id}>
              <strong>{magic.name}</strong>
              {magic.world_id && <span> (World: {magic.world_id})</span>}
              {magic.type && <span> - {magic.type}</span>}
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
};

export default MagicSystems; 