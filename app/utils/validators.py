"""
请求数据验证中间件
自动验证请求数据并返回友好的错误提示
"""

from flask import request, jsonify, g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTExtendedException
from pydantic import ValidationError
from functools import wraps
from app.exceptions.base import (
    ValidationError as BusinessValidationError,
    AuthorizationError,
    NotFoundError,
    QueryError,
)
from app.extensions.extensions import jwt


def validate_request(schema_class):
    """
    装饰器：自动验证请求数据

    使用方法：
    @validate_request(RegisterSchema)
    def register():
        data = g.validated_data
        ...
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                json_data = request.get_json()
                if json_data is None:
                    raise BusinessValidationError("请求体必须是 JSON 格式")

                # 验证数据
                validated = schema_class(**json_data)
                g.validated_data = validated

            except ValidationError as e:
                # Pydantic 验证错误转换为用户友好的消息
                errors = []
                for error in e.errors():
                    field = ".".join(str(x) for x in error["loc"])
                    message = error["msg"]
                    errors.append(f"{field}: {message}")

                raise BusinessValidationError("; ".join(errors), code=40002)
            except ValueError as e:
                raise BusinessValidationError(str(e), code=40002)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_json_content_type():
    """
    检查 Content-Type 是否为 application/json
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method in ["POST", "PUT", "PATCH"]:
                content_type = request.content_type
                if not content_type or "application/json" not in content_type:
                    raise BusinessValidationError(
                        "Content-Type 必须是 application/json", code=40002
                    )
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def login_required():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # verify_jwt_in_request 内部会做以下三件事：
                # 1. 检查有没有 Authorization Header
                # 2. 检查是否有 Bearer 前缀
                # 3. 验证 Token 的合法性和有效期
                verify_jwt_in_request()

                # 只有验证通过，这一步才不会报错
                g.user_id = get_jwt_identity()

            except NoAuthorizationError:
                # 这里的逻辑等同于 if not token
                raise AuthorizationError("请先登录，未检测到认证信息")
            except JWTExtendedException as e:
                # 这里捕获 Token 过期、签名错误等所有 JWT 相关问题
                raise AuthorizationError(f"身份验证无效：{str(e)}")
            except Exception as e:
                print(f"DEBUG JWT ERROR: {type(e).__name__} - {str(e)}")
                raise AuthorizationError("系统处理认证时出错")

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_query(schema_class):
    """
    校验GET请求中query参数
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method != "GET":
                raise NotFoundError(message="请求方式错误")
            try:
                # 使用flat=True防止同名参数只保留一个
                query_data = request.args.to_dict(flat=True)
                g.query_data = schema_class(**query_data)
            except ValidationError as e:
                raise QueryError(message="query参数有误", detail=e.messages)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
