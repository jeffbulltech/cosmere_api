const API_BASE = '/api/v1';

export async function fetchBooks() {
  const res = await fetch(`${API_BASE}/books`);
  if (!res.ok) throw new Error('Failed to fetch books');
  return res.json();
}

export async function fetchCharacters() {
  const res = await fetch(`${API_BASE}/characters`);
  if (!res.ok) throw new Error('Failed to fetch characters');
  return res.json();
}

export async function fetchWorlds() {
  const res = await fetch(`${API_BASE}/worlds`);
  if (!res.ok) throw new Error('Failed to fetch worlds');
  return res.json();
}
