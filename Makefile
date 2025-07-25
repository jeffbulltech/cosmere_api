# Cosmere API Data Pipeline Makefile

# Paths
PARSER=python3 backend/scripts/parse_coppermind_wiki.py
SEEDER=python3 backend/scripts/seed_database.py
MERGE=python3 backend/scripts/merge_data_sources.py
DATA_DIR=backend/data

# Default target: run the full pipeline
all: parse merge seed

# Parse MediaWiki source files to JSON
parse:
	$(PARSER)

# Merge Coppermind and manual character data (optional)
merge:
	$(MERGE)

# Seed the database from JSON files
seed:
	$(SEEDER)

# Remove generated JSON files
clean:
	rm -f $(DATA_DIR)/*.json

bulk-parse:
	python3 backend/scripts/bulk_parse_coppermind_wiki.py uploads

# Activate the Python virtual environment
venv:
	@echo "Activating virtual environment..."
	source cosmere_api_venv/bin/activate

# Start the backend server (must have venv active)
backend:
	@echo "Starting backend server..."
	cd backend && source ../cosmere_api_venv/bin/activate && python3 -c "from app.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"

# Start the backend server in development mode (with venv)
backend-dev:
	@echo "Activating venv and starting backend server on http://127.0.0.1:8000 ..."
	source cosmere_api_venv/bin/activate && cd backend && python3 -c "from app.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"

# Help
help:
	@echo "Cosmere API Data Pipeline Makefile"
	@echo "Targets:"
	@echo "  parse   - Parse MediaWiki files to JSON (backend/data/)"
	@echo "  merge   - Merge Coppermind and manual character data (optional)"
	@echo "  seed    - Seed the database from JSON files"
	@echo "  all     - Run parse, merge, and seed in sequence"
	@echo "  clean   - Remove generated JSON files" 