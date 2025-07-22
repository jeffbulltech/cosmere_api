const API_BASE = '/api/v1';

export async function fetchBooks() {
  const res = await fetch(`${API_BASE}/books/`);
  if (!res.ok) throw new Error('Failed to fetch books');
  const data = await res.json();
  // Return the items array from the paginated response
  return data.items || data;
}

export async function fetchCharacters() {
  const res = await fetch(`${API_BASE}/characters/`);
  if (!res.ok) throw new Error('Failed to fetch characters');
  const data = await res.json();
  return data.items || data;
}

export async function fetchWorlds() {
  const res = await fetch(`${API_BASE}/worlds/`);
  if (!res.ok) throw new Error('Failed to fetch worlds');
  const data = await res.json();
  return data.items || data;
}
