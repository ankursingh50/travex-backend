# models/user.py

from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255)
    mobile_number = fields.CharField(max_length=20, null=True)
    country = fields.CharField(max_length=100, null=True)
    
    user_type = fields.CharField(max_length=20, default='buyer')  # buyer / seller / admin
    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    kyc_profile: fields.ReverseRelation["KYCProfile"]
