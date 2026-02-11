# app/models/user.py
from app.extensions.extensions import db
from datetime import datetime
from collections import OrderedDict


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.BigInteger, unique=True, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    posters = db.relationship(
        "Poster", back_populates="user", cascade="all, delete-orphan"
    )
    # 一对多：一个用户多个 refresh_token
    refresh_tokens = db.relationship(
        "Refresh",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.Index("uq_users_email", "email", unique=True),
        db.Index("uq_users_username", "username", unique=True),
    )

    def to_dict(self):
        return OrderedDict(
            [
                ("user_id", self.user_id),
                ("username", self.username),
                ("email", self.email),
                ("created_at", self.created_at.isoformat()),
                ("updated_at", self.updated_at.isoformat()),
            ]
        )


class Refresh(db.Model):
    __tablename__ = "refresh_tokens"
    id = db.Column(db.Integer, primary_key=True)

    # 外键（核心！）
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id",name="fk_refresh_user_id"),
        nullable=False,
        index=True
    )

    # refresh_token 本体（建议存 hash）
    token = db.Column(db.String(255), unique=True, nullable=False)

    # 是否有效（核心字段）
    is_revoked = db.Column(db.Boolean, default=False)

    # 过期时间
    expires_at = db.Column(db.DateTime, nullable=False)

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 可选：标识设备 / 客户端
    device = db.Column(db.String(64), nullable=True)

    # 反向关系
    user = db.relationship(
        "User",
        back_populates="refresh_tokens"
    )