# app/models/user.py
from app.extensions.extensions import db
from datetime import datetime
from app.models.poster import Poster
from collections import OrderedDict
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    posters = db.relationship(
        "Poster",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.Index('uq_users_email', 'email', unique=True),
        db.Index('uq_users_username', 'username', unique=True),
    )

    def to_dict(self):
        return OrderedDict([
            ("id", self.id),
            ("username", self.username),
            ("email", self.email),
            ("created_at", self.created_at.isoformat()),
            ("updated_at", self.updated_at.isoformat())
        ])
