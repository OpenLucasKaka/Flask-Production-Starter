"""
API 速率限制
防止 API 滥用，保护服务
"""

import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 创建限制器实例
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # 默认限制
    storage_uri=os.getenv("RATE_LIMIT_STORAGE_URI", "memory://"),
)


def setup_rate_limiting(app):
    """初始化速率限制"""
    limiter.init_app(app)
    return limiter
