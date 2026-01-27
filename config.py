import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 所有环境通用设置
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookie 安全通用配置
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
    JWT_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False        # 默认开发环境 False
    REMEMBER_COOKIE_SECURE = False
    JWT_COOKIE_SECURE = False

    # =============== 数据库连接池配置 ===============
    # 最大连接数
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,                    # 保持的连接数
        'pool_recycle': 3600,               # 1小时回收一次连接（防止 MySQL timeout）
        'pool_pre_ping': True,              # 连接前检查是否有效
        'max_overflow': 20,                 # 超过 pool_size 时最多新建的连接数
        'connect_args': {
            'connect_timeout': 10,          # 连接超时时间
            'check_same_thread': False,     # SQLite 特定配置
        }
    }

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")
    )

    # 开发环境 SECRET_KEY 默认值
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret")

    # 开发环境使用较小的连接池
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 10,
    }

class ProConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    JWT_COOKIE_SECURE = True

    # 生产环境使用更大的连接池
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 40,
        'connect_args': {
            'connect_timeout': 10,
        }
    }

    @classmethod
    def check_secrets(cls):
        if not os.environ.get("SECRET_KEY"):
            raise RuntimeError("生产环境必须设置 SECRET_KEY！")
        if not os.environ.get("JWT_SECRET_KEY"):
            raise RuntimeError("生产环境必须设置 JWT_SECRET_KEY！")
        if not os.environ.get("DATABASE_URL"):
            raise RuntimeError("生产环境必须设置 DATABASE_URL！")


config_options = dict(
    development = DevConfig,
    production = ProConfig
)