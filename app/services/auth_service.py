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
    user = User.query.filter(
        and_(User.username == username, User.email == email)
    ).first()
    if not user:
        raise BusinessError("用户不存在", code=40004)

        # 验证密码
    if not bcrypt.check_password_hash(user.password, password):
        raise BusinessError("密码错误", code=40005)

    access_token = create_access_token(identity=str(user.user_id))
    refresh_token = create_refresh_token(
        identity=str(user.user_id), expires_delta=timedelta(days=30)
    )
    refresh_data = Refresh(
        user_id=user.id,
        token=refresh_token,
        is_revoked=True,
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
    user = User.query.filter(user_id == user_id).first()
    if not user:
        raise BusinessError("用户不存在", code=40004)
    return user.to_dict()


def is_user():
    user_id = get_jwt_identity()
    user = User.query.filter(user_id == user_id).first()

    if not user:
        raise BusinessError("用户不存在", code=40004)
    access_token = create_access_token(identity=user_id)
    return {"access_token": access_token}
