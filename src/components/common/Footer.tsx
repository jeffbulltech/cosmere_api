import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-slate-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-cosmere-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">C</span>
              </div>
              <span className="text-xl font-bold text-cosmere-400">Cosmere API</span>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              Explore Brandon Sanderson's Cosmere universe through our comprehensive API and interactive frontend. 
              Discover characters, worlds, magic systems, and their interconnections.
            </p>
            <div className="flex space-x-4">
              <a href="https://github.com" className="text-gray-400 hover:text-cosmere-400 transition-colors">
                GitHub
              </a>
              <a href="https://coppermind.net" className="text-gray-400 hover:text-cosmere-400 transition-colors">
                Coppermind
              </a>
              <a href="https://17thshard.com" className="text-gray-400 hover:text-cosmere-400 transition-colors">
                17th Shard
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/characters" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Characters
                </Link>
              </li>
              <li>
                <Link to="/books" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Books
                </Link>
              </li>
              <li>
                <Link to="/worlds" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Worlds
                </Link>
              </li>
              <li>
                <Link to="/magic-systems" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Magic Systems
                </Link>
              </li>
              <li>
                <Link to="/timeline" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Timeline
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="/api/docs" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  API Documentation
                </a>
              </li>
              <li>
                <a href="/about" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  About
                </a>
              </li>
              <li>
                <a href="/privacy" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="/terms" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="/contact" className="text-gray-300 hover:text-cosmere-400 transition-colors">
                  Contact
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © {currentYear} Cosmere API. All rights reserved.
          </p>
          <p className="text-gray-400 text-sm mt-2 md:mt-0">
            Journey before destination, Radiant.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 