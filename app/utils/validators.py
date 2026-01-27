"""
请求数据验证中间件
自动验证请求数据并返回友好的错误提示
"""
from flask import request, jsonify, g
from pydantic import ValidationError, BaseModel
from functools import wraps
from app.exceptions.base import ValidationError as BusinessValidationError


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
                    raise BusinessValidationError('请求体必须是 JSON 格式')
                
                # 验证数据
                validated = schema_class(**json_data)
                g.validated_data = validated
                
            except ValidationError as e:
                # Pydantic 验证错误转换为用户友好的消息
                errors = []
                for error in e.errors():
                    field = '.'.join(str(x) for x in error['loc'])
                    message = error['msg']
                    errors.append(f"{field}: {message}")
                
                raise BusinessValidationError('; '.join(errors), code=40002)
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
            if request.method in ['POST', 'PUT', 'PATCH']:
                content_type = request.content_type
                if not content_type or 'application/json' not in content_type:
                    raise BusinessValidationError(
                        'Content-Type 必须是 application/json',
                        code=40002
                    )
            return f(*args, **kwargs)
        return decorated_function
    return decorator
