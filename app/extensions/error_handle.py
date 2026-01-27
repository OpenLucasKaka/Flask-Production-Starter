# app/extensions/error_handler.py

from flask import jsonify, g
from app.exceptions.base import (
    BusinessError, ValidationError, AuthenticationError,
    AuthorizationError, NotFoundError, ConflictError,
    RateLimitError, InternalServerError
)
from werkzeug.exceptions import HTTPException
from app.logger import error_logger
import traceback


def register_error_handler(app):
    """注册统一的错误处理器"""
    
    # 业务错误处理
    @app.errorhandler(BusinessError)
    def handle_business_error(e):
        error_logger.warning(
            f"业务错误: {e.message}",
            extra={'code': e.code, 'http_code': e.http_code}
        )
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.message,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.http_code

    # 验证错误
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        error_logger.warning(f"数据验证错误: {e.message}")
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.message,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.http_code

    # 身份认证错误
    @app.errorhandler(AuthenticationError)
    def handle_auth_error(e):
        error_logger.warning(f"身份认证失败: {e.message}")
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.message,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.http_code

    # 权限错误
    @app.errorhandler(AuthorizationError)
    def handle_auth_forbidden(e):
        error_logger.warning(f"权限不足: {e.message}")
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.message,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.http_code

    # 资源不存在
    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        error_logger.warning(f"资源不存在: {e.message}")
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.message,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.http_code

    # 资源冲突
    @app.errorhandler(ConflictError)
    def handle_conflict(e):
        error_logger.warning(f"资源冲突: {e.message}")
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.message,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.http_code

    # 超过速率限制
    @app.errorhandler(RateLimitError)
    def handle_rate_limit(e):
        error_logger.warning(f"速率限制: {e.message}")
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.message,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.http_code

    # HTTP 异常（404, 405, 等）
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        error_logger.warning(f"HTTP 异常: {e.code} {e.name}")
        return jsonify({
            'status': 'error',
            'code': e.code,
            'message': e.description or e.name,
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), e.code

    # 通用异常处理
    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """捕获所有未处理的异常"""
        error_logger.error(
            f"未处理的异常: {str(e)}\n{traceback.format_exc()}"
        )
        
        # 开发环境下返回详细错误信息
        if app.debug or app.config.get('ENV') == 'development':
            return jsonify({
                'status': 'error',
                'code': 50001,
                'message': str(e),
                'request_id': g.get('request_id', 'N/A'),
                'traceback': traceback.format_exc()
            }), 500
        
        # 生产环境下返回通用错误信息
        return jsonify({
            'status': 'error',
            'code': 50001,
            'message': '服务器内部错误',
            'request_id': g.get('request_id', 'N/A'),
            'data': None
        }), 500
