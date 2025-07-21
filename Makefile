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

# Help
help:
	@echo "Cosmere API Data Pipeline Makefile"
	@echo "Targets:"
	@echo "  parse   - Parse MediaWiki files to JSON (backend/data/)"
	@echo "  merge   - Merge Coppermind and manual character data (optional)"
	@echo "  seed    - Seed the database from JSON files"
	@echo "  all     - Run parse, merge, and seed in sequence"
	@echo "  clean   - Remove generated JSON files" 