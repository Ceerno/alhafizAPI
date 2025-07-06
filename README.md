# Quran API

This is a FastAPI-based Quran API that allows users to:

- Retrieve a list of suras from the Quran
- Get the details of a sura by its number (with all its verses)
- Get a verse by sura number and verse number
- Search for verses in Arabic, French, English, or Wolof

## How to Run

1. Install dependencies (already installed if you followed setup):
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
3. Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Endpoints

- `GET /suras` — List all suras
- `GET /suras/{sura_number}` — Get details of a sura (with all its verses)
- `GET /suras/{sura_number}/verses/{verse_number}` — Get a specific verse
- `GET /search?q=...` — Search for verses in Arabic, French, English, or Wolof
- `GET /random-verse` — Get a random verse from the Quran
- `GET /search-suggestions?q=...` — Get autocomplete suggestions for search (unique words from all AyahText fields)

## Data Format

- Suras are loaded from `suras.json` (key: `surahs`)
- Verses are loaded from `verses.json` (key: `verses`)
- Each verse includes fields for Arabic, French, English, Wolof, and an image URL

## Example Usage

**Search for a word or phrase in any language:**

```
GET /search?q=Allah
```

**Get a random verse:**

```
GET /random-verse
```

**Get search suggestions (autocomplete):**

```
GET /search-suggestions?q=mer
```

## Testing

Unit tests are provided in `test_main.py` using pytest and FastAPI's TestClient.

To run the tests:

```bash
pytest test_main.py
```

All main endpoints are covered by tests, including sura/verse retrieval, search, random verse, and search suggestions.

## Note
- The Quran data is loaded from JSON files. Update these files for your needs.
