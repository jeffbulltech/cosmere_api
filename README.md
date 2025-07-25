!["A Cosmere-inspired image from Brandon Sanderson's fantasy universe"](/branding/cosmere_readme_banner.png)

# Cosmere API

### Welcome to the Cosmere API and frontend project! This repository contains:
- A FastAPI backend for Cosmere data
- A React (Vite) frontend for browsing and querying the Cosmere universe

## Quick Start

For full setup instructions, troubleshooting, and development workflow, **see the documentation in the [`/docs` directory](./docs/)**, especially:

- [Development Stack Setup](./docs/dev_stack_setup.md): How to install, run, and debug the backend and frontend locally.
- [Bulk Import Process](./docs/bulk_import.md): How to parse and import MediaWiki source files into the database.

## Project Structure
- `backend/` — FastAPI backend, scripts, and data
- `frontend/` — React app (Vite)
- `docs/` — Documentation for setup, data pipeline, and more

## Contributing
See `/docs` for detailed guides and troubleshooting.

---

For any issues, please consult the docs or open an issue. 

## Backend Development: Using the Python Virtual Environment

All backend development, testing, and server runs should be done with the virtual environment activated. This ensures the correct dependencies and Python version are used.

**To activate the virtual environment:**

```bash
source cosmere_api_venv/bin/activate
```

If you open a new terminal or restart your shell, remember to activate the virtual environment before running backend commands.

--- 