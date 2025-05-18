from fastapi import APIRouter, HTTPException, Query
import os
import httpx

router = APIRouter()

GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

PHOTO_BASE_URL = "https://maps.googleapis.com/maps/api/place/photo"

@router.get("/places/search")
async def search_places(query: str):
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="Google Places API key not configured.")

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    if data["status"] != "OK" or not data["results"]:
        raise HTTPException(status_code=404, detail="No results found.")

    result = data["results"][0]  # Just return the top result

    # Construct photo URL
    photo_url = None
    if "photos" in result:
        photo_ref = result["photos"][0]["photo_reference"]
        photo_url = f"{PHOTO_BASE_URL}?maxwidth=800&photoreference={photo_ref}&key={GOOGLE_API_KEY}"

    return {
        "name": result.get("name"),
        "address": result.get("formatted_address"),
        "rating": result.get("rating"),
        "place_id": result.get("place_id"),
        "photo_url": photo_url
    }
