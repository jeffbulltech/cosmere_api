import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Books from './pages/Books';
import Characters from './pages/Characters';
import Worlds from './pages/Worlds';
import MagicSystems from './pages/MagicSystems';

const App: React.FC = () => {
  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/books">Books</Link></li>
          <li><Link to="/characters">Characters</Link></li>
          <li><Link to="/worlds">Worlds</Link></li>
          <li><Link to="/magic-systems">Magic Systems</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/books" element={<Books />} />
        <Route path="/characters" element={<Characters />} />
        <Route path="/worlds" element={<Worlds />} />
        <Route path="/magic-systems" element={<MagicSystems />} />
        <Route path="*" element={<div>Not Found</div>} />
      </Routes>
    </Router>
  );
};

export default App;
