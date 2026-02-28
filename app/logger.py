import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os

# 日志路径按环境区分
ENV = os.getenv("FLASK_ENV", "development")  # development / production
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if ENV == "development":
    LOG_DIR = os.path.join(BASE_DIR, "../logs/dev")
else:
    LOG_DIR = os.path.join(BASE_DIR, "../logs/prod")

# 日志文件存放路径
os.makedirs(LOG_DIR, exist_ok=True)


# ================= 日志格式（包含 request ID）=================
class RequestIDFilter(logging.Filter):
    """添加 request ID 到日志"""

    def filter(self, record):
        try:
            from flask import g, has_request_context

            if has_request_context():
                record.request_id = g.get("request_id", "N/A")
            else:
                record.request_id = "N/A"
        except RuntimeError:
            # 在应用启动阶段，没有请求上下文
            record.request_id = "N/A"
        return True


formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] [RequestID: %(request_id)s] [%(filename)s:%(lineno)d] %(message)s"
)

# 无 request_id 的格式（用于一般日志）
simple_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(message)s"
)

# ================= 应用/业务日志 =================
app_logger = logging.getLogger("app_logger")
app_logger.setLevel(logging.INFO)
app_logger.addFilter(RequestIDFilter())

app_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8",
)
app_handler.setFormatter(formatter)
if not app_logger.handlers:
    app_logger.addHandler(app_handler)

# ================= 访问日志 =================
access_logger = logging.getLogger("access_logger")
access_logger.setLevel(logging.INFO)
# 不添加 RequestIDFilter，避免日志格式错误
access_logger.propagate = False  # 不传播给根logger

access_handler = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, "access.log"),
    when="midnight",  # 每天新文件
    interval=1,
    backupCount=30,
    encoding="utf-8",
)
access_handler.setFormatter(simple_formatter)
if not access_logger.handlers:
    access_logger.addHandler(access_handler)

# ================= 错误日志 =================
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
error_logger.addFilter(RequestIDFilter())

error_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "error.log"),
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
error_handler.setFormatter(formatter)
if not error_logger.handlers:
    error_logger.addHandler(error_handler)

# # ================= 控制台日志（可选开发用） =================
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# if ENV == "development":
#     app_logger.addHandler(console_handler)
#     access_logger.addHandler(console_handler)
#     error_logger.addHandler(console_handler)

"""
DEBUG   开发阶段调试
INFO    正常业务流程
WARNING 异常预警，但不影响业务
ERROR   业务错误或异常
CRITICAL 系统级别严重错误
"""
