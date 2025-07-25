!["A Cosmere-inspired image from Brandon Sanderson's fantasy universe"](/branding/cosmere_banner.png)

# Cosmere API

## 🌟 Explore the vast universe of Brandon Sanderson's Cosmere

**The Cosmere API** is your gateway to exploring the interconnected worlds, characters, and magic systems of Brandon Sanderson's epic fantasy universe. Whether you're a longtime fan or new to the Cosmere, this platform helps you discover the rich connections between stories spanning multiple series including *The Stormlight Archive*, *Mistborn*, *Elantris*, *Warbreaker*, and more.

### What You Can Discover:

🔍 **Character Connections**: Track characters across different worlds and series, explore their relationships, magic abilities, and cosmic significance

📚 **World Hopping**: Navigate between planets like Roshar, Scadrial, Sel, and Nalthis, understanding their unique cultures, magic systems, and connections

✨ **Magic System Exploration**: Dive deep into the various Investiture systems - from Allomancy and Surgebinding to AonDor and Awakening

🌌 **Cosmere Lore**: Uncover the deeper mysteries of Shards, Adonalsium, and the fundamental forces that bind this universe together

### Perfect For:
- **Fans** wanting to explore character relationships and world connections
- **Readers** looking to understand the broader Cosmere connections
- **Developers** building Cosmere-related applications and tools
- **Researchers** studying the intricate world-building and magic systems

## Roadmap

Find the latest release notes and what's coming for the project in the [ROADMAP](./ROADMAP.md)

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** (recommended: 3.9.6)
- **Node.js 18+** and npm
- **PostgreSQL 13+** (for the database)
- **Git** (for cloning the repository)

### Installation & Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd cosmere_api
```

#### 2. Backend Setup

**Activate the Python Virtual Environment:**
```bash
source cosmere_api_venv/bin/activate
```

**Install Python Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Database Configuration:**
1. Create a PostgreSQL database named `cosmere`
2. Update the database connection in `backend/app/core/config.py`:
   ```python
   DATABASE_URL: str = "postgresql://your_username@localhost/cosmere"
   ```

**Run Database Migrations:**
```bash
cd backend
alembic upgrade head
```

#### 3. Frontend Setup

**Install Node.js Dependencies:**
```bash
cd frontend
npm install
```

### 🏃‍♂️ Starting the Application

#### Option 1: Using Makefile (Recommended)

**Start Backend Server:**
```bash
make backend-dev
```

**Start Frontend Server (in a new terminal):**
```bash
make frontend
```

#### Option 2: Manual Commands

**Backend (with virtual environment activated):**
```bash
cd backend
source ../cosmere_api_venv/bin/activate
python3 -c "from app.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 🌐 Access Points

Once both servers are running:

- **Frontend Application**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/api/v1/docs

### 📁 Project Structure
```
cosmere_api/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── data/         # JSON data files
│   ├── scripts/      # Data import scripts
│   └── migrations/   # Database migrations
├── frontend/         # React app (Vite)
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── package.json  # Dependencies
├── docs/             # Documentation
└── cosmere_api_venv/ # Python virtual environment
```

### 🔧 Development Workflow

#### Backend Development
- Always activate the virtual environment: `source cosmere_api_venv/bin/activate`
- The backend uses FastAPI with SQLAlchemy and PostgreSQL
- API endpoints are available at `/api/v1/`
- Auto-generated documentation at `/api/v1/docs`

#### Frontend Development
- Built with React 18, TypeScript, and Vite
- Uses Tailwind CSS for styling
- API calls are proxied through Vite to the backend
- Hot module replacement enabled for development

### 🐛 Troubleshooting

#### Common Issues

**Backend Issues:**
- **ModuleNotFoundError**: Ensure you're in the `backend/` directory and virtual environment is activated
- **Database Connection Error**: Check PostgreSQL is running and connection string is correct
- **Port Already in Use**: Kill existing processes: `killall python3`

**Frontend Issues:**
- **Port Already in Use**: Vite will automatically try the next available port
- **API Connection Error**: Ensure backend is running on port 8000
- **Build Errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`

#### Environment Setup

**Virtual Environment Management:**
```bash
# Activate (always do this for backend work)
source cosmere_api_venv/bin/activate

# Deactivate when done
deactivate
```

**Database Management:**
```bash
# Check database connection
psql cosmere -c "\dt"

# Run migrations
cd backend && alembic upgrade head

# Reset database (if needed)
cd backend && alembic downgrade base && alembic upgrade head
```

### 📚 Additional Documentation

For detailed guides and advanced topics, see the documentation in the [`/docs` directory](./docs/):

- [Development Stack Setup](./docs/dev_stack_setup.md): Detailed setup instructions
- [Bulk Import Process](./docs/bulk_import.md): Data import workflows
- [API Documentation](./backend/docs/api_documentation.md): API reference
- [Database Schema](./backend/docs/database_schema.md): Database design

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (both frontend and backend)
5. Submit a pull request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.md) file for details.

---

**Need Help?** Check the documentation in [/docs](./docs/) or open an issue for support. 