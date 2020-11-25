from marshmallow import fields, Schema, validate
from marshmallow_enum import EnumField

from src.services.marshmallow import ma
from src.models.users import UserRole


class UserSchema(ma.Schema):
    role = EnumField(UserRole, by_value=True)

    class Meta:
        fields = (
            'id',
            'email',
            'role',
            'first_name',
            'last_name',
            'phone_number',
            'verified'
        )
