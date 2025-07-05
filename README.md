# Quran API

This is a FastAPI-based Quran API that allows users to:

- Retrieve a list of suras from the Quran
- Get the details of a sura by its number
- Get a verse by sura number and verse number

## How to Run

1. Install dependencies (already installed if you followed setup):
   ```bash
   pip install fastapi uvicorn
   ```
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
3. Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Endpoints

- `GET /suras` — List all suras
- `GET /suras/{sura_number}` — Get details of a sura
- `GET /suras/{sura_number}/verses/{verse_number}` — Get a specific verse

## Note
- The Quran data is currently a sample. Replace with full data or connect to a database for production use.
