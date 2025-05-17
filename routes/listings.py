from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from models import BookingListing, User

router = APIRouter()

# Input model for creating a listing
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
    seller_id: int  # Temporary — in future will come from auth token

@router.post("/listings")
async def create_listing(listing: BookingListingIn):
    print("Received listing data:", listing.dict())

    seller = await User.get_or_none(id=listing.seller_id)
    if not seller:
        print("Seller not found!")
        raise HTTPException(status_code=404, detail="Seller not found")

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
