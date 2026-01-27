"""
安全响应头配置
添加常见的安全相关 HTTP 头部
"""


def setup_security_headers(app):
    """
    设置安全响应头
    
    包括：
    - X-Content-Type-Options: 防止 MIME 嗅探
    - X-Frame-Options: 防止点击劫持
    - X-XSS-Protection: 防止 XSS 攻击
    - Strict-Transport-Security: HTTPS 强制
    - Content-Security-Policy: 防止 XSS 和注入攻击
    """
    
    @app.after_request
    def set_security_headers(response):
        # 防止浏览器猜测 MIME 类型
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # 防止网站被 iframe 嵌入（点击劫持防护）
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # 启用浏览器 XSS 防护
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # 内容安全策略（防止 XSS、注入等攻击）
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'"
        )
        
        # 禁用 MIME 类型嗅探
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # 引荐人策略（隐私保护）
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # 强制 HTTPS（仅生产环境）
        if app.config.get('ENV') == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
