"""
认证相关的数据验证模式
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional


class Register(BaseModel):
    """用户注册数据模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=8, max_length=100, description="密码，至少8位")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """验证用户名：只允许字母、数字、下划线"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('用户名只允许字母、数字、下划线和连字符')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """验证密码强度"""
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError('密码必须包含大小写字母和数字')
        return v


class Login(BaseModel):
    """用户登录数据模式"""
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    username: Optional[str] = Field(None, description="用户名")
    password: str = Field(..., description="密码")
    
    @field_validator('email', 'username')
    @classmethod
    def at_least_one_identity(cls, v):
        """确保至少有邮箱或用户名"""
        return v
    
    def model_post_init(self, __context):
        """自定义初始化检查"""
        if not self.email and not self.username:
            raise ValueError('邮箱或用户名至少要填一个')


class ChangePassword(BaseModel):
    """修改密码数据模式"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=8, description="新密码")
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """验证新密码强度"""
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError('新密码必须包含大小写字母和数字')
        return v


class RefreshToken(BaseModel):
    """刷新 token 数据模式"""
    refresh_token: str = Field(..., description="刷新 token")
