# Cosmere API: CRUD Pipeline Using MediaWiki Source Files

This document explains how to **Create, Read, Update, and Delete (CRUD)** Cosmere universe records in the database using MediaWiki source files and the provided data pipeline.

---

## 1. Create or Update a Record

### A. Prepare the Source File
- Obtain or edit the MediaWiki source for a world, book, or character (e.g., `roshar.html`, `the_way_of_kings.html`, `kelsier.html`).
- Save the file in your designated directory (e.g., `/Users/jbthejedi/Documents/`).

### B. Run the Parser Script
- Convert the MediaWiki file(s) into JSON:
  ```bash
  python3 backend/scripts/parse_coppermind_wiki.py
  ```
- This updates `backend/data/worlds.json`, `books.json`, and `characters.json` with the new or updated record(s).

### C. Merge with Existing Data (if needed)
- If combining with other sources (e.g., Coppermind + manual), use the merge script as needed.

### D. Seed the Database
- Load the new/updated JSON data into your database:
  ```bash
  python3 backend/scripts/seed_database.py
  ```
- This creates or updates records in the database based on the JSON files.

---

## 2. Read a Record

- **Via API:**
  - Use FastAPI endpoints to fetch data, e.g.:
    - `GET /api/v1/worlds/roshar`
    - `GET /api/v1/books/the_way_of_kings`
    - `GET /api/v1/characters/kelsier`
- **Directly:**
  - View the JSON files in `backend/data/` or query the database directly.

---

## 3. Update a Record

- **Edit the Source File:**
  - Make changes to the relevant MediaWiki source file.
- **Repeat Steps B–D:**
  - Run the parser, then the seeder, to update the record in the database.

---

## 4. Delete a Record

- **Remove the Entry from the JSON File:**
  - Either:
    - Delete the source file and re-run the parser (to remove it from the JSON).
    - Or manually remove the entry from the relevant JSON file in `backend/data/`.
- **Re-seed the Database:**
  - Run the seeder again:
    ```bash
    python3 backend/scripts/seed_database.py
    ```
  - The seeder will repopulate the database based on the current JSON files.
  - **Note:** The current seeder only adds/updates records; to fully support deletes, you may want to enhance it to remove DB records not present in the JSON.

---

## 5. (Optional) Automate the Pipeline

- You can automate this process with a shell script or Makefile to run the parser and seeder in sequence whenever you add/edit/delete a source file.

---

## Summary Table

| Action   | Step(s)                                                                 |
|----------|-------------------------------------------------------------------------|
| Create   | Add new .html file → Run parser → Run seeder                            |
| Read     | Use API endpoint or view JSON file                                      |
| Update   | Edit .html file → Run parser → Run seeder                               |
| Delete   | Remove from JSON (or .html) → Run parser (if needed) → Run seeder       |

---

## Notes

- **Delete Support:**
  - The current seeder does not remove DB records that are missing from the JSON. For true delete support, enhance `seed_database.py` to remove DB records not present in the JSON file for each entity type.
- **Extensibility:**
  - The parser and pipeline can be extended to support more entity types or more detailed field extraction as needed.
- **Onboarding:**
  - This document is suitable for onboarding new contributors or users to the Cosmere API data pipeline.

---

For questions or improvements, see the main project README or contact the maintainers. 