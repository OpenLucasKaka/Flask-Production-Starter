# Flask-Py 企业级 API 框架

一个现代化的、生产就绪的 Flask 应用框架，包含完整的企业级特性。

## 🎯 核心特性

### 🔐 安全性
- ✅ JWT 身份认证
- ✅ 9 个安全响应头（防 XSS、CSRF、点击劫持等）
- ✅ API 速率限制（防止滥用）
- ✅ 数据验证与清理

### 📊 可观测性
- ✅ 结构化日志（JSON 格式）   
- ✅ 请求追踪 ID（便于问题诊断）
- ✅ Prometheus 监控指标
- ✅ 性能指标收集

### 🛠️ 开发体验
- ✅ Swagger 文档（有需要可使用）
- ✅ Pydantic 数据验证
- ✅ 统一的错误处理与响应格式
- ✅ 完整的单元测试框架

### 🚀 生产就绪
- ✅ 数据库连接池配置
- ✅ 健康检查接口（`/health`, `/readiness`）
- ✅ 多环境配置支持
- ✅ 环境变量验证
- ✅ Docker 容器化部署
- ✅ Prometheus + Grafana 监控可视化

---

## ⚡ 快速启动

### Docker Compose 一键启动（推荐）
```bash
docker-compose up
```

**服务访问地址：**
| 服务 | 地址 | 用途 |
|------|------|------|
| Flask API | http://localhost:8000 | REST API 和 Swagger 文档 |
| Prometheus | http://localhost:9090 | 时间序列数据库和指标查询 |
| Grafana | http://localhost:3000 | 可视化仪表板（默认密码：admin） |

### 本地开发启动
```bash
# 安装依赖并启动
uv sync && flask run
```

---

## 🏗️ 项目结构

```
flask_py/
├── app/
│   ├── controller/          # API 路由层
│   │   ├── auth.py         # 认证相关端点
│   │   ├── health.py       # 健康检查
│   │   └── message.py      # 消息相关端点
│   ├── services/           # 业务逻辑层
│   ├── models/             # 数据模型（ORM）
│   ├── schemas/            # Pydantic 数据验证模式
│   ├── exceptions/         # 自定义异常
│   ├── extensions/         # Flask 扩展配置
│   │   ├── error_handle.py       # 错误处理
│   │   ├── extensions.py         # 扩展初始化
│   │   ├── prometheus_metrics.py # 监控指标
│   │   ├── rate_limiting.py      # 速率限制
│   │   ├── security_headers.py   # 安全头
│   │   ├── structured_logging.py # 结构化日志
│   │   └── swagger.py            # API 文档
│   └── utils/
│       ├── __init__.py           # 响应格式化
│       ├── env_validator.py      # 环境变量验证
│       └── validators.py         # 数据验证装饰器
├── tests/                   # 单元测试
│   ├── conftest.py         # 测试配置和 fixtures
│   └── test_api.py         # API 测试
├── migrations/             # 数据库迁移
├── logs/                   # 日志输出目录
├── config.py              # 应用配置
├── pyproject.toml         # 项目依赖和元数据
├── Dockerfile             # 容器化配置
├── docker-compose.yml     # 本地开发环境
└── README.md              # 本文档
```

---

## 🚀 快速开始

### 环境要求
- Python 3.11+
- Docker & Docker Compose（可选）

### 本地开发

#### 1. 克隆项目
```bash
git clone <repository>
cd flask_py
```

#### 2. 创建并激活虚拟环境（uv 自动完成）
```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate

# 环境安装flask
pip install flask
# 推荐使用 uv（自动创建虚拟环境，速度快 5 倍）

uv sync
```

#### 3. 环境配置
```bash
cp .env.example .env
# 编辑 .env 配置
```

#### 4. 初始化数据库
```bash
flask db init
flask db migrate
flask db upgrade
```

#### 5. 运行应用
```bash
# 开发模式 (可二选一)

1. python run.py
2. flask run

# 生产模式（使用 Gunicorn）
gunicorn -c gunicorn.conf.py wsgi:app
```

开发环境应用将在 `http://localhost:5000` 运行。
模拟生产环境应用将在 `http://127.0.0.1:8000` 运行。

---


## 代码格式化
```bash
uv run flake8 app tests //检查是否存在代码未格式化

pip install black //使用black格式化代码
black .
```

## 🔍 API 文档

### Swagger UI
访问 `http://localhost:5000/api/v1/docs` 查看交互式 API 文档(需要打开api的路由)

### 主要端点

#### 健康检查
- `GET /health` - 基本健康状态
- `GET /readiness` - 就绪检查（包括数据库）

#### 认证
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录

#### 监控
- `GET /metrics` - Prometheus 指标

---

## 📋 响应格式

### 成功响应
```json
{
    "status": "success",
    "code": "200",
    "message": "success",
    "data": {},
    "request_id": "uuid"
}
```

### 错误响应
```json
{
    "status": "error",
    "code": "40001",
    "message": "错误描述",
    "request_id": "uuid",
    "data": null
}
```

---

## 🧪 测试

### 运行测试
```bash
# 使用 uv 运行测试
uv run pytest -v

# 生成覆盖率报告
uv run pytest --cov=app --cov-report=html
```

# 使用脚本运行
bash run_tests.sh
```

### 测试覆盖率目标
- 当前目标：> 60%
- 关键路径：> 80%

---

## 🐳 Docker 部署

### 构建镜像
```bash
docker build -t flask_py:latest .
```

### 运行容器
```bash
# 开发环境（包含 Prometheus 和 Grafana）
docker-compose up

# 仅运行 Flask 应用
docker run -p 8000:8000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-key \
  flask_py:latest
```

### 本地开发环境启动

#### 方式 1：使用 Docker Compose（推荐）
```bash
# 一键启动所有服务（Flask + Prometheus + Grafana）
docker-compose up

# 访问地址：
# - Flask API:      http://localhost:8000
# - Prometheus:     http://localhost:9090
# - Grafana:        http://localhost:3000
```

#### 方式 2：本地运行（需要 Python 3.11+）
```bash
# 1. 安装依赖（自动创建虚拟环境）
uv sync

# 2. 启动 Flask 开发服务器
uv run flask run

# 4. 如需监控，手动启动 Prometheus 和 Grafana
# Prometheus (需单独安装)
prometheus --config.file=prometheus.yml

# Grafana (Docker)
docker run -d -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana:latest
```

### Grafana 使用指南

#### 首次登录
1. 访问 `http://localhost:3000`
2. 默认账号：`admin`
3. 默认密码：`admin`
4. 首次登录会提示修改密码

#### 添加 Prometheus 数据源
1. 进入 **Configuration** → **Data Sources**
2. 点击 **Add data source**
3. 选择 **Prometheus**
4. URL 填入：`http://prometheus:9090`
5. 点击 **Save & Test**

#### 导入仪表板
1. 进入 **+ → Import**
2. 输入仪表板 ID 或粘贴 JSON
3. 推荐的 Prometheus 仪表板：
   - ID 3662: Prometheus 服务器监控
   - ID 1860: Node Exporter 完整版

#### 创建自定义仪表板
示例查询（PromQL）：
```promql
# 请求速率
rate(flask_requests_total[5m])

# 平均响应时间
avg(flask_request_duration_seconds_bucket)

# 错误率
rate(flask_errors_total[5m])

# 活跃请求数
flask_active_requests
```

### Kubernetes 部署
```bash
# 创建 ConfigMap
kubectl create configmap flask-config --from-file=.env

# 应用部署配置
kubectl apply -f k8s/
```

---

## 📊 监控和日志

### Prometheus 指标
访问 `http://localhost:8000/metrics` 查看 Prometheus 格式的指标

关键指标：
- `flask_requests_total` - 请求总数
- `flask_request_duration_seconds` - 请求耗时分布
- `flask_active_requests` - 当前活跃请求数
- `flask_errors_total` - 错误总数

### 日志查看
```bash
# 实时查看日志
tail -f logs/dev/access.log

# 查看错误日志
tail -f logs/dev/error.log
```

---

## ⚙️ 配置管理

### 环境变量
```bash
# 必需的
FLASK_ENV=development|production
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://user:pass@localhost/dbname

# 可选的
DEBUG=True|False
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
```

### 数据库配置
配置文件在 `config.py` 中定义：
- **开发环境**：SQLite（5 个连接池）
- **生产环境**：PostgreSQL（20 个连接池）

---

## 🔒 安全建议

### 生产环境检查清单
- [ ] 设置强随机的 `SECRET_KEY` 和 `JWT_SECRET_KEY`
- [ ] 使用 HTTPS（在负载均衡器或反向代理级别）
- [ ] 配置数据库备份
- [ ] 设置日志聚合（ELK Stack）
- [ ] 启用 CORS 白名单
- [ ] 定期更新依赖（检查安全漏洞）
- [ ] 设置 WAF（Web 应用防火墙）
- [ ] 监控异常请求模式

---


## 🛠️ 开发工具链

### 代码质量
```bash
# 代码风格检查
flake8 app/

# 类型检查
mypy app/

# 代码格式化
black app/
```

### 依赖管理
```bash
# 使用 uv 管理依赖（更快）
uv sync

# 或者使用 pip
pip install -e .
```

---

## 📚 相关文档

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Prometheus 文档](https://prometheus.io/docs/)

---

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 更新日志

### v1.0.0 (2026-01-26)
- ✨ 初始版本发布
- 🔐 完整的身份认证系统
- 📊 Prometheus 监控
- 🧪 单元测试框架
- 📖 API 文档
- 🔒 安全响应头

---

## 📧 联系方式

如有问题或建议，欢迎提交 Issue 或 PR。

---

**Made with ❤️ for production-ready Flask applications**