from tortoise import fields, models
from enum import Enum


class RoleType(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(unique=True, index=True, max_length=255)
    password = fields.TextField(null=True)
    role = fields.CharEnumField(RoleType)
    display_name = fields.TextField(null=True)
    email = fields.TextField(null=True)
    phone = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
