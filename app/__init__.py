import os

from flask import Flask

from app.extensions.extensions import register_extensions
from app.extensions.request_tracking import setup_request_tracking
from app.extensions.structured_logging import setup_structured_logging
from app.extensions.prometheus_metrics import setup_prometheus
from app.extensions.security_headers import setup_security_headers
from config import config_options,ProConfig
from flask import request

def create_app():
    app = Flask(__name__)

    # app_config = config_options[os.getenv("FLASK_ENV","development")]
    env = os.getenv("FLASK_ENV","development")
    app_config = config_options[env]
    app.config.from_object(app_config)
    if env == "production":
        app_config.check_secrets()

    register_extensions(app)
    
    # 注册请求追踪中间件
    setup_request_tracking(app)
    
    # 注册 Prometheus 监控
    setup_prometheus(app)
    
    # 注册安全响应头
    setup_security_headers(app)

    from app.controller import auth_bp, health_bp
    # from app.extensions.swagger import api_bp  //swagger文档
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(health_bp, url_prefix="")
    # app.register_blueprint(api_bp)

    from .logger import app_logger,access_logger,error_logger
    app.logger.handlers = app_logger.handlers
    app.logger.setLevel(app_logger.level)
    
    # 设置结构化日志
    setup_structured_logging(app)

    @app.before_request
    def log_request_info():
        access_logger.info(f"访问路径: {request.path}, 方法: {request.method}")

    @app.errorhandler(Exception)
    def handle_exception(e):
        error_logger.exception("捕获异常")
        return {"error": str(e)}, 500

    # 避免使用 `import app.models` 否则会在此作用域中覆盖 `app` 变量
    # 使用 importlib 动态导入模型包
    import importlib
    importlib.import_module('app.models')

    from app.extensions.error_handle import register_error_handler
    register_error_handler(app)

    return app

