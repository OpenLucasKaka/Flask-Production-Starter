"""
Prometheus 监控配置示例

使用方法：
1. 启动 Prometheus（docker-compose 中）
2. 配置 Prometheus 采集 Flask 应用的 /metrics 端点
3. 在 Grafana 中创建仪表板展示这些指标

关键指标：
- flask_requests_total: 请求总数（按方法、端点、状态分组）
- flask_request_duration_seconds: 请求耗时分布
- flask_active_requests: 当前活跃请求数
- flask_errors_total: 错误总数
"""

# 如果使用 docker-compose，将以下内容添加到 docker-compose.yml 中：
"""
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  prometheus_data:
  grafana_data:
"""

# prometheus.yml 配置示例：
"""
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask-app'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
"""
