# Bulk Import Process for Cosmere MediaWiki Source Files

This document describes how to use the automated bulk import pipeline to parse and ingest multiple MediaWiki source files (e.g., from Coppermind) into the Cosmere API database.

## Overview
- **Purpose:** Quickly process a directory of MediaWiki `.html` files, extract structured data (worlds, books, characters), and populate the database.
- **Components:**
  - `backend/scripts/bulk_parse_coppermind_wiki.py`: Bulk parser script
  - `Makefile`: `bulk-parse` target for easy execution
  - `backend/data/`: Output directory for combined JSON files
  - `backend/uploads/`: Default directory for raw `.html` files to import

## Step-by-Step Usage

### 1. Place Source Files
Copy or move all MediaWiki `.html` files you wish to import into the `backend/uploads/` directory. Each file should contain the raw source for a world, book, or character page.

### 2. Run the Bulk Parser
From the project root, run:

```
make bulk-parse
```

This will:
- Parse all `.html` files in `backend/uploads/`
- Classify each as a world, book, or character (based on infobox/template)
- Write combined `worlds.json`, `books.json`, and `characters.json` to `backend/data/`

### 3. Seed the Database
After parsing, run:

```
make seed
```

This will populate the database with the newly parsed data.

## Custom Input Directory
To use a different directory for your `.html` files, run the script directly:

```
python3 backend/scripts/bulk_parse_coppermind_wiki.py <your_directory>
```

## Troubleshooting
- **File Not Classified:** If a file cannot be classified, a warning will be printed. Ensure the file contains a recognizable infobox (e.g., `{{book`, `{{character`, `{{shardworld`).
- **Output Missing Data:** Check the output JSON files in `backend/data/` for completeness. If data is missing, review the source files for formatting issues.
- **Database Errors:** If seeding fails, check for missing required fields (e.g., world IDs) in the JSON files.

## Extending the Pipeline
- To support new entity types or infoboxes, update the classification logic in `bulk_parse_coppermind_wiki.py`.
- For advanced validation or error reporting, enhance the parser scripts as needed.

---

For further help, see the main project documentation or contact the maintainers. 