"""
环境变量验证工具
在应用启动时检查必要的环境变量和配置
"""
import os
from app.logger import app_logger


class EnvironmentValidator:
    """环境变量验证器"""
    
    # 所有环境都需要的变量
    REQUIRED_COMMON = [
        'FLASK_ENV',
    ]
    
    # 生产环境必需的变量
    REQUIRED_PRODUCTION = [
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'DATABASE_URL',
    ]
    
    # 可选的但推荐配置的变量
    RECOMMENDED = [
        'LOG_LEVEL',
    ]
    
    # 默认值
    DEFAULTS = {
        'FLASK_ENV': 'development',
        'LOG_LEVEL': 'INFO',
    }
    
    @classmethod
    def validate(cls):
        """
        验证环境变量
        
        Raises:
            EnvironmentError: 如果缺少必要的环境变量
        """
        env = os.getenv('FLASK_ENV', 'development')
        
        # 检查必需的通用变量
        missing_vars = []
        for var in cls.REQUIRED_COMMON:
            if not os.getenv(var):
                missing_vars.append(var)
        
        # 检查环境特定的必需变量
        if env == 'production':
            for var in cls.REQUIRED_PRODUCTION:
                if not os.getenv(var):
                    missing_vars.append(var)
        
        if missing_vars:
            error_msg = f"缺少必需的环境变量: {', '.join(missing_vars)}"
            app_logger.error(error_msg)
            raise EnvironmentError(error_msg)
        
        # 检查推荐的变量
        missing_recommended = []
        for var in cls.RECOMMENDED:
            if not os.getenv(var):
                missing_recommended.append(var)
        
        if missing_recommended:
            app_logger.warning(
                f"推荐设置以下环境变量: {', '.join(missing_recommended)}"
            )
        
        # 打印环境信息
        app_logger.info(f"应用环境: {env}")
        app_logger.info(f"DEBUG 模式: {os.getenv('DEBUG', 'False')}")
        
        return True
    
    @classmethod
    def set_defaults(cls):
        """
        设置默认的环境变量
        （只对未设置的变量有效）
        """
        for key, value in cls.DEFAULTS.items():
            if not os.getenv(key):
                os.environ[key] = value
                app_logger.info(f"使用默认值: {key}={value}")
