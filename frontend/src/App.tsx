import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Books from './pages/Books';

const App: React.FC = () => {
  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/books">Books</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/books" element={<Books />} />
        {/* Add more routes here as needed */}
        <Route path="*" element={<div>Not Found</div>} />
      </Routes>
    </Router>
  );
};

export default App;
