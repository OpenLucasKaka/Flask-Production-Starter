from app import create_app
from app.utils.env_validator import EnvironmentValidator

# 在应用启动前验证环境变量
EnvironmentValidator.set_defaults()
EnvironmentValidator.validate()

app = create_app()
