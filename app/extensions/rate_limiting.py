"""
API 速率限制
防止 API 滥用，保护服务
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request
from flask import current_app

# 创建限制器实例
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # 默认限制
    storage_uri="memory://",  # 使用内存存储（生产建议用 Redis）
)


def setup_rate_limiting(app):
    """初始化速率限制"""
    limiter.init_app(app)
    
    # 可选：为特定路由添加自定义限制,也可单独进行接口级限流
    @app.before_request
    def before_request_limits():
        #
        # if request.endpoint == 'health':
        #     return  # 放行
        #
        # if request.endpoint == 'login':
        #     limiter.limit("5 per minute")(current_app.view_functions[request.endpoint])
        pass
    
    return limiter
