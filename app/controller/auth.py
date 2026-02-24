"""
示例业务模块：认证相关 API 端点
"""

from flask import g
from flask_jwt_extended import jwt_required
from app.controller import auth_bp
from app.exceptions.base import BusinessError
from app.schemas.auth import Register, Login
from app.services import register_user
from app.services.auth_service import user_login, user_profile, is_user
from app.utils import success, error
from app.utils.validators import validate_request, validate_json_content_type
from app.extensions.rate_limiting import limiter


@auth_bp.route("/")
def index():
    return success(data="ok", code="200", message="ok", http_code=200)


@auth_bp.route("/ping")
def ping():
    return "pong"


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per hour")  # 注册：5次/小时
@validate_json_content_type()
@validate_request(Register)
def register():
    """用户注册"""
    data = g.validated_data
    try:
        result = register_user(data)
        return success(result)
    except ValueError as e:
        return error(code="400", message=str(e))
    except Exception:
        raise


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per hour")  # 登录：10次/小时
@validate_json_content_type()
@validate_request(Login)
def login():
    """用户登录"""
    data = g.validated_data
    email = data.email
    username = data.username
    password = data.password

    try:
        result = user_login(email, username, password)
        return success(result)
    except ValueError as e:
        return error(code="400", message=str(e))
    except Exception:
        raise


@auth_bp.route("/profile/<user_id>", methods=["GET"])
@validate_json_content_type()
def profile(user_id):
    """用户信息"""
    result = user_profile(user_id)
    return success(result)


@auth_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refesh():
    try:
        result = is_user()
        return success(result)
    except BusinessError as e:
        return error(code="400", message=str(e))
