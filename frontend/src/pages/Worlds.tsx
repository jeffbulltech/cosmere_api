import React from 'react';
import WorldList from '../components/worlds/WorldList';

const Worlds: React.FC = () => {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Cosmere Worlds</h1>
        <p className="text-gray-600">
          Journey through the diverse worlds of Brandon Sanderson's Cosmere universe. 
          Each world has its own unique magic systems, cultures, and stories waiting to be discovered.
        </p>
      </div>
      
      <WorldList />
    </div>
  );
};

export default Worlds;
