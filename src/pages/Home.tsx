import React from 'react';
import { Link } from 'react-router-dom';
import { 
  UserGroupIcon, 
  BookOpenIcon, 
  GlobeAltIcon, 
  SparklesIcon,
  MagnifyingGlassIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

const Home: React.FC = () => {
  const features = [
    {
      name: 'Characters',
      description: 'Explore detailed character profiles with relationships, magic abilities, and appearances across books.',
      icon: UserGroupIcon,
      href: '/characters',
      color: 'bg-cosmere-500',
    },
    {
      name: 'Books',
      description: 'Browse the complete Cosmere bibliography with reading order, summaries, and world connections.',
      icon: BookOpenIcon,
      href: '/books',
      color: 'bg-roshar-500',
    },
    {
      name: 'Worlds',
      description: 'Discover the diverse worlds of the Cosmere with maps, cultures, and magic systems.',
      icon: GlobeAltIcon,
      href: '/worlds',
      color: 'bg-scadrial-500',
    },
    {
      name: 'Magic Systems',
      description: 'Learn about the unique magic systems that power each world in the Cosmere.',
      icon: SparklesIcon,
      href: '/magic-systems',
      color: 'bg-purple-500',
    },
    {
      name: 'Advanced Search',
      description: 'Search across all content with intelligent filters and cross-references.',
      icon: MagnifyingGlassIcon,
      href: '/search',
      color: 'bg-green-500',
    },
    {
      name: 'Timeline',
      description: 'Explore the chronological events and connections across the Cosmere universe.',
      icon: ChartBarIcon,
      href: '/timeline',
      color: 'bg-orange-500',
    },
  ];

  const stats = [
    { name: 'Characters', value: '500+' },
    { name: 'Books', value: '20+' },
    { name: 'Worlds', value: '10+' },
    { name: 'Magic Systems', value: '15+' },
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-16 bg-gradient-to-br from-slate-900 via-slate-800 to-cosmere-900 rounded-2xl">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Explore the{' '}
            <span className="text-cosmere-400">Cosmere</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Discover Brandon Sanderson's interconnected universe through our comprehensive API and interactive frontend. 
            Journey through worlds, meet characters, and unravel the mysteries of the Cosmere.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/characters"
              className="btn-primary text-lg px-8 py-3"
            >
              Start Exploring
            </Link>
            <Link
              to="/search"
              className="btn-secondary text-lg px-8 py-3"
            >
              Search Everything
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat) => (
            <div key={stat.name} className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-cosmere-600 mb-2">
                {stat.value}
              </div>
              <div className="text-gray-600 font-medium">{stat.name}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Everything You Need to Explore the Cosmere
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            From character relationships to world maps, our comprehensive database covers every aspect of Brandon Sanderson's universe.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <Link
              key={feature.name}
              to={feature.href}
              className="card-hover group"
            >
              <div className="flex items-center mb-4">
                <div className={`p-3 rounded-lg ${feature.color} text-white mr-4 group-hover:scale-110 transition-transform duration-200`}>
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 group-hover:text-cosmere-600 transition-colors">
                  {feature.name}
                </h3>
              </div>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </Link>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-cosmere-50 rounded-2xl p-8 md:p-12">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Dive Deeper?
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Whether you're a first-time reader or a seasoned Cosmere scholar, our tools will enhance your understanding of this vast universe.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/characters"
              className="btn-primary"
            >
              Browse Characters
            </Link>
            <Link
              to="/worlds"
              className="btn-secondary"
            >
              Explore Worlds
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home; 