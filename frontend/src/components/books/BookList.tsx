import React, { useEffect, useState } from 'react';
import { fetchBooks } from '../../services/api';

type Book = {
  id: string;
  title: string;
  world_id?: string;
  series_id?: string;
};

const BookList: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBooks()
      .then(setBooks)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading books...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Books</h2>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            <strong>{book.title}</strong>
            {book.world_id && <span> (World: {book.world_id})</span>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BookList;
