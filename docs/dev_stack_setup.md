# Cosmere API & Frontend Development Stack Setup

This guide explains how to set up and run the full Cosmere API backend and React frontend for local development.

---

## 1. Prerequisites
- Python 3.9+
- Node.js (v18+ recommended) & npm
- (Recommended) Use a Python virtual environment

---

## 2. Backend (FastAPI) Setup

### a. Install Python dependencies
From the project root:
```sh
cd cosmere_api_venv  # or activate your venv if not already
cd ..
pip install -r requirements.txt
```

### b. Create or check your FastAPI app
- The main app should be in `backend/app/main.py` and contain:
  ```python
  from fastapi import FastAPI
  app = FastAPI()
  @app.get("/api/v1/books")
  def get_books():
      return [{"id": "test-book", "title": "Test Book", "world_id": "roshar"}]
  ```

### c. Run the backend server
```sh
uvicorn backend.app.main:app --reload --port 5241
```
- If you get an error about the port being in use, try another (e.g., 5242).
- If you get an error about `app` not found, make sure your FastAPI instance is named `app`.

### d. Test the backend
Visit [http://localhost:5241/api/v1/books](http://localhost:5241/api/v1/books) in your browser. You should see JSON output.

---

## 3. Frontend (React + Vite) Setup

### a. Install Node dependencies
From the `frontend` directory:
```sh
cd frontend
npm install
```

### b. Vite Proxy Configuration
Edit `frontend/vite.config.ts` to include:
```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:5241'
    }
  }
});
```

### c. Start the frontend dev server
```sh
npm run dev
```
- Note the port Vite reports (e.g., 5173, 5174, 5175, etc.).
- Open [http://localhost:517X/](http://localhost:517X/) in your browser.

### d. Test the frontend
- Navigate to `/books` (e.g., [http://localhost:517X/books](http://localhost:517X/books)).
- You should see the test book from the backend.

---

## 4. Troubleshooting

- **ERR_CONNECTION_REFUSED:**
  - Make sure both backend and frontend servers are running.
  - Double-check the port numbers.
- **Unexpected token '<', "<!DOCTYPE"... is not valid JSON:**
  - The frontend is not reaching the backend. Check Vite proxy config and backend port.
- **Cannot find module '@vitejs/plugin-react':**
  - Run `npm install @vitejs/plugin-react --save-dev` in the frontend directory.
- **Error loading ASGI app. Attribute "app" not found:**
  - Ensure your FastAPI instance is named `app` in `main.py`.
- **404 for /favicon.ico:**
  - This is harmless and can be ignored.

---

## 5. Useful Commands
- **Start backend:**
  ```sh
  uvicorn backend.app.main:app --reload --port 5241
  ```
- **Start frontend:**
  ```sh
  cd frontend
  npm run dev
  ```
- **Install frontend dependencies:**
  ```sh
  npm install
  ```
- **Install missing Vite plugin:**
  ```sh
  npm install @vitejs/plugin-react --save-dev
  ```

---

## 6. Next Steps
- Implement real API endpoints and connect to your database.
- Expand the frontend to browse characters, worlds, etc.
- See other docs in `/docs` for data pipeline and API usage. 