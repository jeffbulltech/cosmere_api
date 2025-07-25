import React from 'react';
import MagicSystemList from '../components/magic_systems/MagicSystemList';

const MagicSystems: React.FC = () => {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Cosmere Magic Systems</h1>
        <p className="text-gray-600">
          Explore the diverse and intricate magic systems that power Brandon Sanderson's Cosmere universe. 
          Each system has its own rules, limitations, and unique abilities.
        </p>
      </div>
      
      <MagicSystemList />
    </div>
  );
};

export default MagicSystems; 