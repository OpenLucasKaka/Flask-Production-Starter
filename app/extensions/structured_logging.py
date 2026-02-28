"""
结构化日志系统
提供 JSON 格式的日志输出，便于日志聚合和分析
"""

import json
import logging
from datetime import datetime, timezone

from flask import g, has_request_context, request


class JSONFormatter(logging.Formatter):
    """JSON 格式的日志格式化器"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # 添加请求上下文信息
        if has_request_context():
            log_data["request_id"] = g.get("request_id", "N/A")
            log_data["http_method"] = request.method
            log_data["http_path"] = request.path
            log_data["http_remote_addr"] = request.remote_addr

        # 如果有异常信息，添加到日志
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_structured_logging(app):
    """
    设置结构化日志
    在生产环境可以将日志输出重定向到 ELK Stack 进行收集和分析
    """
    # 根据环境选择是否使用 JSON 格式
    env = app.config.get("ENV", "development")

    if env == "production":
        # 生产环境使用 JSON 格式
        json_formatter = JSONFormatter()

        for handler in app.logger.handlers:
            handler.setFormatter(json_formatter)

        # 也为其他应用级别的日志使用 JSON 格式
        for logger_name in ("app_logger", "access_logger", "error_logger"):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers:
                handler.setFormatter(json_formatter)
