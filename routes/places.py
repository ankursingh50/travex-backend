from fastapi import APIRouter, HTTPException, Query, Response
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

    result = data["results"][0]

    photo_url = None
    if "photos" in result:
        photo_ref = result["photos"][0]["photo_reference"]
        photo_url = f"/places/photo?ref={photo_ref}"

    return {
        "name": result.get("name"),
        "address": result.get("formatted_address"),
        "rating": result.get("rating"),
        "place_id": result.get("place_id"),
        "photo_url": photo_url
    }

@router.get("/places/photo")
async def get_place_photo(ref: str = Query(...), maxwidth: int = Query(800)):
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="Google API key not configured.")

    params = {
        "photoreference": ref,
        "maxwidth": maxwidth,
        "key": GOOGLE_API_KEY
    }

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(PHOTO_BASE_URL, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch image")

        return Response(
            content=response.content,
            media_type=response.headers.get("content-type", "image/jpeg")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
