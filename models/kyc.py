# models/kyc.py

from tortoise import fields
from tortoise.models import Model
from enum import Enum

class KYCStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class KYCProfile(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="kyc_profile", on_delete=fields.CASCADE)

    gov_id_type = fields.CharField(max_length=100, null=True)
    gov_id_number = fields.CharField(max_length=100, null=True)
    gov_id_image_url = fields.TextField(null=True)

    address = fields.TextField(null=True)
    country = fields.CharField(max_length=100, null=True)

    status = fields.CharEnumField(KYCStatus, default=KYCStatus.pending)
    rejection_reason = fields.TextField(null=True)

    submitted_at = fields.DatetimeField(auto_now_add=True)
    reviewed_at = fields.DatetimeField(null=True)
