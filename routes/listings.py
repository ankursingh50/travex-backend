from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
# from models import BookingListing, User
from models.user import User
import httpx
import os

router = APIRouter()

# ✅ Helper to fetch Google Places data
async def fetch_google_place_data(query: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://maps.googleapis.com/maps/api/place/textsearch/json",
            params={"query": query, "key": os.getenv("GOOGLE_PLACES_API_KEY")}
        )
        result = response.json()["results"][0]
        photo_ref = result.get("photos", [{}])[0].get("photo_reference")
        photo_url = (
            f"https://maps.googleapis.com/maps/api/place/photo"
            f"?maxwidth=800&photoreference={photo_ref}&key={os.getenv('GOOGLE_PLACES_API_KEY')}"
            if photo_ref else None
        )
        return {
            "place_id": result.get("place_id"),
            "google_photo_url": photo_url,
            "google_rating": result.get("rating"),
            "google_address": result.get("formatted_address")
        }

# ✅ Input model for creating a listing
class BookingListingIn(BaseModel):
    hotel_name: str
    location: str
    check_in: date
    check_out: date
    number_of_guests: int
    room_type: str
    amenities: Optional[List[str]] = []
    original_price: float
    resale_price: float
    voucher_image_url: str
    hotel_images: Optional[List[str]] = []
    payout_account: str
    seller_id: int
    rating: Optional[float] = 0.0

# ✅ POST endpoint to create listing
@router.post("/listings")
async def create_listing(listing: BookingListingIn):
    print("Received listing data:", listing.dict())

    seller, _ = await User.get_or_create(
        id=listing.seller_id,
        defaults={"email": f"test{listing.seller_id}@travex.com"}
    )

    # ✅ Fetch from Google
    google_info = await fetch_google_place_data(f"{listing.hotel_name} {listing.location}")

    print("Creating listing for seller:", seller.email)

    new_listing = await BookingListing.create(
        hotel_name=listing.hotel_name,
        location=listing.location,
        check_in=listing.check_in,
        check_out=listing.check_out,
        number_of_guests=listing.number_of_guests,
        room_type=listing.room_type,
        amenities=", ".join(listing.amenities) if listing.amenities else None,
        original_price=listing.original_price,
        resale_price=listing.resale_price,
        voucher_image_url=listing.voucher_image_url,
        hotel_images=listing.hotel_images,
        payout_account=listing.payout_account,
        seller=seller,
        rating=listing.rating,
        place_id=google_info.get("place_id"),
        google_photo_url=google_info.get("google_photo_url"),
        google_rating=google_info.get("google_rating"),
        google_address=google_info.get("google_address"),
    )

    print("Listing created with ID:", new_listing.id)

    return {
        "id": new_listing.id,
        "hotel_name": new_listing.hotel_name,
        "resale_price": float(new_listing.resale_price),
        "check_in": str(new_listing.check_in),
        "check_out": str(new_listing.check_out),
        "status": new_listing.status,
    }

# ✅ GET endpoint with filtering
@router.get("/listings")
async def get_filtered_listings(
    location: Optional[str] = Query(None),
    check_in: Optional[date] = Query(None),
    max_price: Optional[float] = Query(None),
    min_rating: Optional[float] = Query(None),
    sort_by: Optional[str] = Query(None, description="Options: price_asc, price_desc, rating")
):
    query = BookingListing.all().prefetch_related("seller")

    if location:
        query = query.filter(location__icontains=location)
    if check_in:
        query = query.filter(check_in__gte=check_in)
    if max_price is not None:
        query = query.filter(resale_price__lte=max_price)
    if min_rating is not None:
        query = query.filter(rating__gte=min_rating)

    if sort_by == "price_asc":
        query = query.order_by("resale_price")
    elif sort_by == "price_desc":
        query = query.order_by("-resale_price")
    elif sort_by == "rating":
        query = query.order_by("-rating")

    listings = await query

    return [
        {
            "id": listing.id,
            "hotel_name": listing.hotel_name,
            "location": listing.location,
            "check_in": str(listing.check_in),
            "check_out": str(listing.check_out),
            "room_type": listing.room_type,
            "resale_price": float(listing.resale_price),
            "original_price": float(listing.original_price),
            "rating": float(listing.rating or 0),
            "google_rating": listing.google_rating,
            "google_photo_url": listing.google_photo_url,
            "google_address": listing.google_address,
            "place_id": listing.place_id,
            "amenities": listing.amenities.split(", ") if listing.amenities else [],
            "hotel_images": listing.hotel_images or [],
            "voucher_image_url": listing.voucher_image_url,
            "seller_email": listing.seller.email,
            "status": listing.status
        }
        for listing in listings
    ]
