import React from 'react';
import BookList from '../components/books/BookList';

const Books: React.FC = () => {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Cosmere Books</h1>
        <p className="text-gray-600">
          Explore the vast collection of books that make up Brandon Sanderson's Cosmere universe. 
          From epic fantasy to science fiction, discover the stories that connect across worlds.
        </p>
      </div>
      
      <BookList />
    </div>
  );
};

export default Books;
