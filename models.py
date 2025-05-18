from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

class BookingListing(Model):
    id = fields.IntField(pk=True)

    hotel_name = fields.CharField(max_length=255)
    location = fields.CharField(max_length=255)
    check_in = fields.DateField()
    check_out = fields.DateField()
    number_of_guests = fields.IntField()
    room_type = fields.CharField(max_length=100)
    amenities = fields.TextField(null=True)
    rating = fields.FloatField(default=0.0)

    original_price = fields.DecimalField(max_digits=10, decimal_places=2)
    resale_price = fields.DecimalField(max_digits=10, decimal_places=2)

    voucher_image_url = fields.CharField(max_length=512)
    hotel_images = fields.JSONField(null=True)

    payout_account = fields.CharField(max_length=255)

    # New fields to store Google Places metadata
    place_id = fields.CharField(max_length=255, null=True)
    google_photo_url = fields.CharField(max_length=1024, null=True)
    google_rating = fields.FloatField(null=True)
    google_address = fields.TextField(null=True)

    seller = fields.ForeignKeyField("models.User", related_name="listings")

    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)
    status = fields.CharField(max_length=50, default="pending")

    class Meta:
        table = "booking_listings"

