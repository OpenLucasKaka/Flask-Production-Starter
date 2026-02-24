"""
Prometheus 监控指标
method = GET / POST / PUT / DELETE
endpoint = Flask 给每个路由起的“内部名字”，不是 URL
status = 200 / 400 / 401 / 500
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import request, g
import time

# 定义指标
request_count = Counter(
    "flask_requests_total", "Flask 请求总数", ["method", "endpoint", "status"]
)

request_duration = Histogram(
    "flask_request_duration_seconds", "Flask 请求耗时（秒）", ["method", "endpoint"]
)

request_size = Histogram(
    "flask_request_size_bytes", "Flask 请求大小（字节）", ["method", "endpoint"]
)

response_size = Histogram(
    "flask_response_size_bytes", "Flask 响应大小（字节）", ["method", "endpoint"]
)

active_requests = Gauge("flask_active_requests", "Flask 当前活跃请求数")

error_count = Counter("flask_errors_total", "Flask 错误总数", ["type", "status"])


def setup_prometheus(app):
    """初始化 Prometheus 监控"""

    @app.before_request
    def before_request_metrics():
        """记录请求开始时间和活跃请求数"""
        g.metrics_start_time = time.time()
        active_requests.inc()

    @app.after_request
    def after_request_metrics(response):
        """记录请求指标"""
        try:
            # 计算耗时
            duration = time.time() - getattr(g, "metrics_start_time", time.time())

            # 获取端点信息
            method = request.method
            endpoint = request.endpoint or "unknown"
            status = response.status_code

            # 记录请求计数
            request_count.labels(method=method, endpoint=endpoint, status=status).inc()

            # 记录请求耗时
            request_duration.labels(method=method, endpoint=endpoint).observe(duration)

            # 记录请求大小
            request_size.labels(method=method, endpoint=endpoint).observe(
                request.content_length or 0
            )

            # 记录响应大小
            try:
                response_data_len = len(response.get_data())
            except RuntimeError:
                # 处理 passthrough 响应（如文件下载等）
                response_data_len = 0
            response_size.labels(method=method, endpoint=endpoint).observe(
                response_data_len
            )

            # 错误统计
            if status >= 400:
                error_count.labels(type="http_error", status=status).inc()
        finally:
            # 减少活跃请求数
            active_requests.dec()

        return response

    # 添加 /metrics 端点
    @app.route("/metrics")
    def metrics():
        """Prometheus metrics 端点"""
        return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}
