from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
import json
import os
import random

app = FastAPI(title="Quran API", description="API to retrieve Quran suras and verses", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SURAS_PATH = os.path.join(BASE_DIR, "suras.json")
VERSES_PATH = os.path.join(BASE_DIR, "verses.json")



# --- Random Verse Endpoint ---
@app.get(
    "/random-verse",
    response_model=Dict,
    summary="Get a random verse",
    description="Returns a random verse from the Quran."
)
def get_random_verse():
    """
    Returns a random verse from the Quran.
    """
    verses = load_verses()
    verse = random.choice(verses)
    return verse

# --- Search Suggestions Autocomplete Endpoint ---
@app.get(
    "/search-suggestions",
    response_model=List[str],
    summary="Get search suggestions (autocomplete)",
    description="Returns a list of unique words from all AyahText fields for autocomplete suggestions. Optional query parameter 'q' will filter suggestions."
)
def search_suggestions(q: str = Query(None, description="Partial word to autocomplete")):
    """
    Returns a list of unique words from all AyahText fields for autocomplete suggestions.
    If 'q' is provided, only suggestions containing 'q' (case-insensitive) are returned.
    """
    verses = load_verses()
    words = set()
    for v in verses:
        for field in ("AyahText", "AyahTextFr", "AyahTextEng", "AyahTextWf"):
            text = v.get(field)
            if text:
                for word in text.split():
                    words.add(word.strip('.,;:!?"\'«»()[]{}'))
    suggestions = sorted(words)
    if q:
        q_lower = q.lower()
        suggestions = [w for w in suggestions if q_lower in w.lower()]
    return suggestions

@app.get(
    "/search",
    response_model=List[Dict],
    summary="Search verses",
    description="Search for verses containing the query in any AyahText field (Arabic, French, English, Wolof)."
)
def search_verses(q: str = Query(..., description="Search query")):
    """
    Search for verses containing the query in any AyahText field (Arabic, French, English, Wolof).
    - **q**: The search query string. Case-insensitive. Matches in Arabic, French, English, or Wolof fields.
    """
    verses = load_verses()
    q_lower = q.lower()
    results = []
    for v in verses:
        if (
            (v.get("AyahText") and q_lower in v["AyahText"].lower()) or
            (v.get("AyahTextFr") and q_lower in v["AyahTextFr"].lower()) or
            (v.get("AyahTextEng") and q_lower in v["AyahTextEng"].lower()) or
            (v.get("AyahTextWf") and q_lower in v["AyahTextWf"].lower())
        ):
            results.append(v)
    return results

def load_suras():
    with open(SURAS_PATH, encoding="utf-8") as f:
        data = json.load(f)
        return data["surahs"]

def load_verses():
    with open(VERSES_PATH, encoding="utf-8") as f:
        data = json.load(f)
        return data["verses"]

@app.get("/suras", response_model=List[Dict])
def get_suras():
    """Retrieve list of all suras."""
    suras = load_suras()
    return suras

@app.get("/suras/{sura_number}", response_model=Dict)
def get_sura_detail(sura_number: int):
    """Get details of a sura by its number, including all its verses."""
    suras = load_suras()
    verses = load_verses()
    sura = next((s for s in suras if int(s["SuraID"]) == sura_number), None)
    if not sura:
        raise HTTPException(status_code=404, detail="Sura not found")
    sura_verses = [v for v in verses if int(v["sourates_id"]) == sura_number]
    sura_detail = sura.copy()
    sura_detail["verses"] = sura_verses
    return sura_detail

@app.get("/suras/{sura_number}/verses/{verse_number}", response_model=Dict)
def get_verse(sura_number: int, verse_number: int):
    """Get a verse by sura number and verse number."""
    suras = load_suras()
    verses = load_verses()
    # Find the sura
    sura = next((s for s in suras if int(s["SuraID"]) == sura_number), None)
    if not sura:
        raise HTTPException(status_code=404, detail="Sura not found")
    # Find the verse
    verse = next((v for v in verses if int(v["sourates_id"]) == sura_number and int(v["VerseID"]) == verse_number), None)
    if not verse:
        raise HTTPException(status_code=404, detail="Verse not found")
    return {
        "sura_number": sura_number,
        "sura_name": sura["SuraNom"],
        "verse_number": verse_number,
        "AyahText": verse["AyahText"],
        "AyahTextFr": verse["AyahTextFr"],
        "AyahTextEng": verse["AyahTextEng"],
        "AyahTextWf": verse["AyahTextWf"],
        "image": verse["image"]
    }
