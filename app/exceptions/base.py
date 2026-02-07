"""
自定义异常类
提供统一的错误处理机制
"""


class BusinessError(Exception):
    """业务逻辑错误"""

    def __init__(self, message, code=40001, http_code=400):
        self.message = message
        self.code = code
        self.http_code = http_code


class ValidationError(BusinessError):
    """数据验证错误"""

    def __init__(self, message, code=40002):
        super().__init__(message, code=code, http_code=400)


class AuthenticationError(BusinessError):
    """身份认证错误"""

    def __init__(self, message, code=40101):
        super().__init__(message, code=code, http_code=401)


class AuthorizationError(BusinessError):
    """权限错误"""

    def __init__(self, message, code=40301):
        super().__init__(message, code=code, http_code=403)


class NotFoundError(BusinessError):
    """资源不存在"""

    def __init__(self, message="资源不存在", code=40401):
        super().__init__(message, code=code, http_code=404)


class ConflictError(BusinessError):
    """资源冲突（如重复的用户名）"""

    def __init__(self, message, code=40901):
        super().__init__(message, code=code, http_code=409)


class RateLimitError(BusinessError):
    """超过速率限制"""

    def __init__(self, message="请求过于频繁，请稍后再试", code=42901):
        super().__init__(message, code=code, http_code=429)


class InternalServerError(BusinessError):
    """内部服务器错误"""

    def __init__(self, message="服务器内部错误", code=50001):
        super().__init__(message, code=code, http_code=500)


class QueryError(BusinessError):
    """query参数错误"""

    def __init__(self, message="query参数有误", code=40003):
        super().__init__(message, code, http_code=400)
