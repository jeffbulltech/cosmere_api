import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  const sections = [
    {
      title: 'Characters',
      description: 'Explore the rich cast of characters that populate Brandon Sanderson\'s Cosmere universe.',
      icon: '👥',
      path: '/characters',
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    {
      title: 'Books',
      description: 'Discover the books and series that make up the Cosmere, from Mistborn to Stormlight Archive.',
      icon: '📚',
      path: '/books',
      color: 'bg-green-500 hover:bg-green-600'
    },
    {
      title: 'Worlds',
      description: 'Journey through the diverse worlds of the Cosmere, each with its own unique magic and culture.',
      icon: '🌍',
      path: '/worlds',
      color: 'bg-purple-500 hover:bg-purple-600'
    },
    {
      title: 'Magic Systems',
      description: 'Learn about the intricate magic systems that power the Cosmere universe.',
      icon: '✨',
      path: '/magic-systems',
      color: 'bg-yellow-500 hover:bg-yellow-600'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to the Cosmere API
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Explore the vast universe created by Brandon Sanderson. From worldhoppers to magic systems, 
          discover the interconnected stories that make up the Cosmere.
        </p>
      </div>

      {/* Navigation Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {sections.map((section) => (
          <Link
            key={section.path}
            to={section.path}
            className="group block bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200"
          >
            <div className="p-6">
              <div className={`w-12 h-12 rounded-lg ${section.color} flex items-center justify-center text-white text-2xl mb-4 group-hover:scale-110 transition-transform duration-200`}>
                {section.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {section.title}
              </h3>
              <p className="text-gray-600 text-sm">
                {section.description}
              </p>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick Stats */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Overview</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">100+</div>
            <div className="text-sm text-gray-600">Characters</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">20+</div>
            <div className="text-sm text-gray-600">Books</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">10+</div>
            <div className="text-sm text-gray-600">Worlds</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">15+</div>
            <div className="text-sm text-gray-600">Magic Systems</div>
          </div>
        </div>
      </div>

      {/* About Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">About the Cosmere</h2>
        <p className="text-gray-600 mb-4">
          The Cosmere is a fictional universe created by Brandon Sanderson, consisting of multiple worlds 
          connected by a shared magic system and mythology. Each world has its own unique magic system, 
          but they all follow the same underlying rules and are connected by the presence of Shards of Adonalsium.
        </p>
        <p className="text-gray-600">
          This API provides comprehensive data about characters, books, worlds, and magic systems, 
          allowing you to explore the rich tapestry of stories that make up the Cosmere universe.
        </p>
      </div>
    </div>
  );
};

export default Home;
