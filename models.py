from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

class BookingListing(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    check_in = fields.DateField()
    check_out = fields.DateField()
    seller = fields.ForeignKeyField("models.User", related_name="listings")
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)
