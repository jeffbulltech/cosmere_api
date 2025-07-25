import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import ErrorBoundary from './components/common/ErrorBoundary';
import Home from './pages/Home';
import Books from './pages/Books';
import Characters from './pages/Characters';
import Worlds from './pages/Worlds';
import MagicSystems from './pages/MagicSystems';
import CharacterDetail from './pages/CharacterDetail';
import BookDetail from './pages/BookDetail';
import WorldDetail from './pages/WorldDetail';
import MagicSystemDetail from './pages/MagicSystemDetail';
import SeriesDetail from './pages/SeriesDetail';
import ShardDetail from './pages/ShardDetail';

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen flex flex-col">
          <Header />
          <main className="flex-1 bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/books" element={<Books />} />
                <Route path="/characters" element={<Characters />} />
                <Route path="/worlds" element={<Worlds />} />
                <Route path="/magic-systems" element={<MagicSystems />} />
                
                {/* Detail Pages */}
                <Route path="/characters/:id" element={<CharacterDetail />} />
                <Route path="/books/:id" element={<BookDetail />} />
                <Route path="/worlds/:id" element={<WorldDetail />} />
                <Route path="/magic-systems/:id" element={<MagicSystemDetail />} />
                <Route path="/series/:id" element={<SeriesDetail />} />
                <Route path="/shards/:id" element={<ShardDetail />} />
                
                <Route path="*" element={
                  <div className="text-center py-12">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">404 - Page Not Found</h1>
                    <p className="text-gray-600 mb-8">The page you're looking for doesn't exist.</p>
                    <a 
                      href="/" 
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                    >
                      Go Home
                    </a>
                  </div>
                } />
              </Routes>
            </div>
          </main>
          <Footer />
        </div>
      </Router>
    </ErrorBoundary>
  );
};

export default App;
