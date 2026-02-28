from flask import jsonify, g, has_request_context
from app.exceptions.base import (
    BusinessError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    InternalServerError,  # noqa: F401
)
from werkzeug.exceptions import HTTPException
from app.logger import error_logger
import traceback


def _request_id():
    if has_request_context():
        return g.get("request_id", "N/A")
    return "N/A"


def _error_response(code, message, http_code):
    return (
        jsonify(
            {
                "status": "error",
                "code": code,
                "message": message,
                "request_id": _request_id(),
                "data": None,
            }
        ),
        http_code,
    )


def register_error_handler(app):
    """注册统一的错误处理器"""

    # 业务错误处理
    @app.errorhandler(BusinessError)
    def handle_business_error(e):
        error_logger.warning(
            "业务错误: %s", e.message, extra={"code": e.code, "http_code": e.http_code}
        )
        return _error_response(e.code, e.message, e.http_code)

    # 验证错误
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        error_logger.warning("数据验证错误: %s", e.message)
        return _error_response(e.code, e.message, e.http_code)

    # 身份认证错误
    @app.errorhandler(AuthenticationError)
    def handle_auth_error(e):
        error_logger.warning("身份认证失败: %s", e.message)
        return _error_response(e.code, e.message, e.http_code)

    # 权限错误
    @app.errorhandler(AuthorizationError)
    def handle_auth_forbidden(e):
        error_logger.warning("权限不足: %s", e.message)
        return _error_response(e.code, e.message, e.http_code)

    # 资源不存在
    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        error_logger.warning("资源不存在: %s", e.message)
        return _error_response(e.code, e.message, e.http_code)

    # 资源冲突
    @app.errorhandler(ConflictError)
    def handle_conflict(e):
        error_logger.warning("资源冲突: %s", e.message)
        return _error_response(e.code, e.message, e.http_code)

    # 超过速率限制
    @app.errorhandler(RateLimitError)
    def handle_rate_limit(e):
        error_logger.warning("速率限制: %s", e.message)
        return _error_response(e.code, e.message, e.http_code)

    # HTTP 异常（404, 405, 等）
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        error_logger.warning("HTTP 异常: %s %s", e.code, e.name)
        return _error_response(e.code, e.description or e.name, e.code)

    # 通用异常处理
    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """捕获所有未处理的异常"""
        error_logger.error("未处理的异常: %s\n%s", str(e), traceback.format_exc())

        # 开发环境下返回详细错误信息
        if app.debug or app.config.get("ENV") == "development":
            return (
                jsonify(
                    {
                        "status": "error",
                        "code": 50001,
                        "message": str(e),
                        "request_id": _request_id(),
                        "traceback": traceback.format_exc(),
                    }
                ),
                500,
            )

        # 生产环境下返回通用错误信息
        return _error_response(50001, "服务器内部错误", 500)
