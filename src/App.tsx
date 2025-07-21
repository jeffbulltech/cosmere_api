import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import Characters from './pages/Characters';
import Books from './pages/Books';
import Worlds from './pages/Worlds';
import Search from './pages/Search';
import NotFound from './pages/NotFound';
import { ApiProvider } from './contexts/ApiContext';
import { SearchProvider } from './contexts/SearchContext';
import { ThemeProvider } from './contexts/ThemeContext';

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <ApiProvider>
          <SearchProvider>
            <MainLayout>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/characters" element={<Characters />} />
                <Route path="/books" element={<Books />} />
                <Route path="/worlds" element={<Worlds />} />
                <Route path="/search" element={<Search />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </MainLayout>
          </SearchProvider>
        </ApiProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App; 