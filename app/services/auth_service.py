import hashlib
from datetime import timedelta, datetime

from app.exceptions.base import BusinessError
from app.models.user import User, Refresh
from app.extensions.extensions import db, bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from sqlalchemy import or_, and_
from app.utils.snowflake import snowflake


def _hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _find_user_by_identity(user_identity):
    user = User.query.filter(User.user_id == user_identity).first()
    if not user:
        raise BusinessError("用户不存在", code=40004, http_code=404)
    return user


def register_user(data):
    email = data.email.strip() if data.email else None
    username = data.username.strip()
    if not email:
        raise ValueError("邮箱不能为空")
    if not username:
        raise ValueError("用户名不能为空")
    if User.query.filter(or_(User.email == email, User.username == username)).first():
        raise ValueError("用户名或邮箱已存在")
    password_hash = bcrypt.generate_password_hash(data.password).decode("utf-8")
    user_id = snowflake.generate()
    user = User(username=username, password=password_hash, email=email, user_id=user_id)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise BusinessError("注册失败，请重试", code=500)
    return user.to_dict()


def user_login(email, username, password):
    if not email and not username:
        raise BusinessError("邮箱或用户名至少填写一个", code=40002, http_code=400)

    filters = []
    if email:
        filters.append(User.email == email)
    if username:
        filters.append(User.username == username)

    user = User.query.filter(and_(*filters)).first()
    if not user:
        raise BusinessError("用户不存在", code=40004, http_code=404)

        # 验证密码
    if not bcrypt.check_password_hash(user.password, password):
        raise BusinessError("密码错误", code=40005)

    access_token = create_access_token(identity=str(user.user_id))
    refresh_token = create_refresh_token(
        identity=str(user.user_id), expires_delta=timedelta(days=30)
    )
    refresh_data = Refresh(
        user_id=user.id,
        token=_hash_refresh_token(refresh_token),
        is_revoked=False,
        expires_at=datetime.utcnow() + timedelta(days=30),
    )
    try:
        db.session.add(refresh_data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise BusinessError("获取token失败请重试", code=40006)
    return {**user.to_dict(), "token": access_token, "refresh": refresh_token}


def user_profile(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    if not user:
        raise BusinessError("用户不存在", code=40004, http_code=404)
    return user.to_dict()


def is_user():
    user_id = get_jwt_identity()
    user = User.query.filter(User.user_id == user_id).first()

    if not user:
        raise BusinessError("用户不存在", code=40004, http_code=404)
    access_token = create_access_token(identity=user_id)
    return {"access_token": access_token}


def rotate_refresh_token(raw_refresh_token: str):
    user_identity = get_jwt_identity()
    user = _find_user_by_identity(user_identity)

    current_record = Refresh.query.filter_by(
        user_id=user.id,
        token=_hash_refresh_token(raw_refresh_token),
        is_revoked=False,
    ).first()

    if not current_record:
        raise BusinessError("refresh token 无效或已撤销", code=40102, http_code=401)

    if current_record.expires_at <= datetime.utcnow():
        current_record.is_revoked = True
        db.session.commit()
        raise BusinessError("refresh token 已过期", code=40103, http_code=401)

    access_token = create_access_token(identity=str(user.user_id))
    new_refresh_token = create_refresh_token(
        identity=str(user.user_id), expires_delta=timedelta(days=30)
    )

    current_record.is_revoked = True
    next_record = Refresh(
        user_id=user.id,
        token=_hash_refresh_token(new_refresh_token),
        is_revoked=False,
        expires_at=datetime.utcnow() + timedelta(days=30),
    )
    db.session.add(next_record)
    db.session.commit()

    return {"access_token": access_token, "refresh_token": new_refresh_token}


def revoke_refresh_token(raw_refresh_token: str):
    user_identity = get_jwt_identity()
    user = _find_user_by_identity(user_identity)

    record = Refresh.query.filter_by(
        user_id=user.id,
        token=_hash_refresh_token(raw_refresh_token),
        is_revoked=False,
    ).first()
    if not record:
        raise BusinessError("refresh token 无效或已撤销", code=40102, http_code=401)

    record.is_revoked = True
    db.session.commit()
    return {"revoked": True}
