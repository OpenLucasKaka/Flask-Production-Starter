"""
请求追踪中间件
为每个请求生成唯一的 request ID，用于日志追踪
"""

import uuid
import time
from flask import request, g


def generate_request_id():
    """生成唯一的请求 ID"""
    return str(uuid.uuid4())


def setup_request_tracking(app):
    """
    设置请求追踪中间件

    在每个请求前生成追踪 ID，放入 g 对象和响应头
    所有日志都会包含该 ID，便于追踪完整的请求链路
    """

    @app.before_request
    def before_request():
        # 从请求头获取或生成新的 request ID
        request_id = request.headers.get("X-Request-ID") or generate_request_id()
        g.request_id = request_id
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        # 在响应头中添加 request ID
        response.headers["X-Request-ID"] = g.get("request_id", "")

        # 记录请求耗时
        if hasattr(g, "start_time"):
            elapsed = time.time() - g.start_time
            response.headers["X-Response-Time"] = f"{elapsed:.3f}s"

        return response


def get_request_id():
    """获取当前请求的 ID"""
    return g.get("request_id", "unknown")
