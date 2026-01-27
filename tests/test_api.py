"""
API 基础端点测试
"""
import pytest


class TestHealthCheck:
    """健康检查端点测试"""
    
    def test_health_endpoint(self, client):
        """测试 /health 端点"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'
    
    def test_readiness_endpoint(self, client):
        """测试 /readiness 端点"""
        response = client.get('/readiness')
        assert response.status_code in [200, 503]  # 可能因数据库而异
        assert 'status' in response.json


class TestAuthEndpoints:
    """认证端点测试"""
    
    def test_ping_endpoint(self, client):
        """测试 ping 端点"""
        response = client.get('/auth/ping')
        assert response.status_code == 200
        assert response.data == b'pong'
    
    def test_index_endpoint(self, client):
        """测试首页端点"""
        response = client.get('/auth/')
        assert response.status_code == 200
        assert response.json['status'] == 'success'


class TestMetricsEndpoint:
    """Prometheus 指标端点测试"""
    
    def test_metrics_endpoint(self, client):
        """测试 /metrics 端点"""
        response = client.get('/metrics')
        assert response.status_code == 200
        # 应该返回 Prometheus 格式的数据
        assert b'flask_requests_total' in response.data or b'HELP' in response.data


class TestRequestTracking:
    """请求追踪功能测试"""
    
    def test_request_id_in_response_header(self, client):
        """测试响应头中包含 request_id"""
        response = client.get('/auth/')
        assert 'X-Request-ID' in response.headers
        assert response.headers['X-Request-ID']  # 应该不为空
    
    def test_response_time_in_header(self, client):
        """测试响应头中包含响应时间"""
        response = client.get('/auth/')
        assert 'X-Response-Time' in response.headers


class TestErrorHandling:
    """错误处理测试"""
    
    def test_404_error(self, client):
        """测试 404 错误"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        assert response.json['status'] == 'error'
    
    def test_method_not_allowed(self, client):
        """测试方法不允许"""
        response = client.post('/auth/')
        assert response.status_code == 405


class TestRateLimiting:
    """速率限制测试"""
    
    def test_register_rate_limiting(self, client):
        """测试注册端点的速率限制"""
        # 这个测试可能需要多次请求来触发限制
        # 实际测试需要根据配置调整
        pass
