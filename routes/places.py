# routes/places.py

from fastapi import APIRouter, Query, HTTPException
import os
import httpx

router = APIRouter()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

@router.get("/places/search")
async def search_places(query: str = Query(..., description="Hotel name + city")):
    if not GOOGLE_PLACES_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    params = {
        "query": query,
        "key": GOOGLE_PLACES_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_PLACES_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Google Places")

    return response.json()
