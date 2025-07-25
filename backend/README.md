# Cosmere API Backend

A comprehensive FastAPI backend for exploring Brandon Sanderson's Cosmere universe.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust relational database
- **Redis** - High-performance caching layer
- **Elasticsearch** - Full-text search capabilities
- **Docker** - Containerized development environment
- **Alembic** - Database migration management
- **Structured Logging** - Comprehensive logging with structlog
- **OpenAPI Documentation** - Auto-generated API documentation

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

## 🛠️ Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cosmere_api/backend
   ```

2. **Start the development environment**
   ```bash
   ./scripts/start-dev.sh
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/api/v1/docs
   - Health Check: http://localhost:8000/health
   - Root Endpoint: http://localhost:8000/

### Option 2: Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start PostgreSQL and Redis**
   ```bash
   docker-compose up -d postgres redis
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/          # API endpoint modules
│   │       └── api.py             # Main API router
│   ├── core/
│   │   ├── config.py              # Application configuration
│   │   ├── database.py            # Database setup
│   │   └── logging.py             # Logging configuration
│   ├── models/                    # SQLAlchemy models
│   ├── schemas/                   # Pydantic schemas
│   ├── services/                  # Business logic services
│   └── main.py                    # Application entry point
├── data/                          # JSON data files
├── migrations/                    # Alembic migrations
├── scripts/                       # Utility scripts
├── tests/                         # Test suite
├── docker-compose.yml            # Docker services
├── Dockerfile                    # Application container
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `env.example` to `.env` and customize:

```bash
# Application Settings
APP_NAME=cosmere-api
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://cosmere_user:cosmere_password@localhost:5432/cosmere_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200
```

## 📚 API Endpoints

### Books
- `GET /api/v1/books` - List all books
- `GET /api/v1/books/{book_id}` - Get specific book
- `GET /api/v1/books/{book_id}/characters` - Get book characters

### Characters
- `GET /api/v1/characters` - List all characters
- `GET /api/v1/characters/{character_id}` - Get specific character
- `GET /api/v1/characters/{character_id}/relationships` - Get character relationships

### Worlds
- `GET /api/v1/worlds` - List all worlds
- `GET /api/v1/worlds/{world_id}` - Get specific world
- `GET /api/v1/worlds/{world_id}/magic-systems` - Get world magic systems
- `GET /api/v1/worlds/{world_id}/characters` - Get world characters

### Series
- `GET /api/v1/series` - List all series
- `GET /api/v1/series/{series_id}` - Get specific series
- `GET /api/v1/series/{series_id}/books` - Get series books

### Magic Systems
- `GET /api/v1/magic-systems` - List all magic systems
- `GET /api/v1/magic-systems/{magic_system_id}` - Get specific magic system
- `GET /api/v1/magic-systems/{magic_system_id}/users` - Get magic system users

### Shards
- `GET /api/v1/shards` - List all shards
- `GET /api/v1/shards/{shard_id}` - Get specific shard
- `GET /api/v1/shards/{shard_id}/vessels` - Get shard vessels

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_books.py
```

## 🗄️ Database

### Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Data Import

```bash
# Import data from JSON files
python scripts/import_data.py
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

## 📝 Development Guidelines

### Code Style

- Use **Black** for code formatting
- Use **isort** for import sorting
- Use **flake8** for linting

```bash
# Format code
black app/

# Sort imports
isort app/

# Lint code
flake8 app/
```

### Git Workflow

1. Create feature branch: `git checkout -b feature/description`
2. Make changes and commit: `git commit -m "feat: add new endpoint"`
3. Push and create pull request

### Commit Message Format

Use conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Maintenance tasks

## 🔍 Monitoring

- **Health Check**: `GET /health`
- **Metrics**: Prometheus metrics (planned)
- **Logging**: Structured JSON logs

## 🚀 Deployment

### Production

1. Set `ENVIRONMENT=production`
2. Configure production database and Redis
3. Set secure `SECRET_KEY`
4. Use production Docker setup

### Environment Variables

```bash
# Production settings
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secure-secret-key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/api/v1/docs`
- Review the logs for debugging information
