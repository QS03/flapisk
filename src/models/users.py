"""Users  models and database functionality"""
from enum import Enum
from sqlalchemy import func
from src.services.db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class UserRole(Enum):
    ADMIN = "Admin"
    USER = "User"
    DEVELOPER = "Developer"

    @classmethod
    def role(cls, role):
        if role == "Admin":
            return cls.ADMIN
        elif role == "User":
            return cls.USER
        elif role == "Developer":
            return cls.DEVELOPER
        else:
            return "Invalid Role"


class UserModel(db.Model):
    """Model class to represent users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    first_name = db.Column(db.String(256), nullable=True)
    last_name = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(256), nullable=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_at = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id} ({self.email}), role: {self.role or '[no role]'}>"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    @classmethod
    def get_first(cls, filters):
        return cls.query.filter(*filters).first()

    @classmethod
    def get_all(cls, filters):
        return cls.query.filter(*filters).all()
