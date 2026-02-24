# Flask Production Starter

一个可直接用于业务开发的 Flask 后端模板。

它提供生产项目常见的基础能力：认证、统一错误处理、请求追踪、结构化日志、Prometheus 指标、限流、测试、CI、Docker。

## 1. 项目定位

- 目标：作为后端项目初始化模板，帮助你快速进入业务开发
- 形态：模板能力 + 示例业务模块（`auth` / `poster`）
- 非目标：不绑定某个行业业务，不做“大而全业务系统”

## 2. 你可以直接得到什么

- JWT 认证（注册、登录、refresh）
- 统一错误响应格式
- 请求追踪（`X-Request-ID`）
- 响应耗时头（`X-Response-Time`）
- Prometheus 指标（`/metrics`）
- 接口限流（Flask-Limiter）
- 安全响应头
- SQLAlchemy + Flask-Migrate
- Pytest + 覆盖率、flake8、black、mypy
- GitHub Actions CI
- Docker / Docker Compose

## 3. 目录结构

```text
├── app/
│   ├── controller/            # 路由层（HTTP 入口）
│   ├── services/              # 业务层（核心逻辑）
│   ├── models/                # 数据模型（SQLAlchemy）
│   ├── schemas/               # 请求参数模型（Pydantic）
│   ├── exceptions/            # 业务异常定义
│   ├── extensions/            # 横切能力（日志/监控/限流/错误处理等）
│   └── utils/                 # 工具与校验
├── tests/
├── docs/
├── config.py
├── run.py
├── wsgi.py
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

## 4. 环境要求

- Python `3.11+`
- 建议使用 `uv`（也支持 pip）
- 可选：Docker / Docker Compose

## 5. 快速启动

### 5.1 本地开发

```bash
# 1) 安装依赖
uv sync

# 2) 配置环境变量
cp .env.example .env

# 3) 启动服务
python run.py
```

默认地址：`http://127.0.0.1:5000`

### 5.2 Docker Compose

> `docker-compose.yml` 使用 production 配置，必须提供密钥。

```bash
export SECRET_KEY='replace-this'
export JWT_SECRET_KEY='replace-this'
docker compose up --build
```

服务地址：

- API: `http://localhost:8000`
- Prometheus: `http://localhost:9091`
- Grafana: `http://localhost:3000`

## 6. 环境变量说明

| 变量名 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `FLASK_ENV` | 否 | `development` | 运行环境：`development`/`production` |
| `SECRET_KEY` | 生产必填 | 无 | Flask 密钥 |
| `JWT_SECRET_KEY` | 生产必填 | 无 | JWT 签名密钥 |
| `DATABASE_URL` | 生产必填 | `sqlite:///data-dev.sqlite` | 数据库连接串 |
| `LOG_LEVEL` | 否 | `INFO` | 日志等级 |
| `RATE_LIMIT_STORAGE_URI` | 否 | `memory://` | 限流存储，生产建议 Redis |

## 7. 核心接口

### 健康检查

- `GET /health`
- `GET /readiness`

### 认证

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/profile/<user_id>`
- `GET /auth/refresh`

### 示例业务

- `POST /poster/add`
- `GET /poster/list`

### 监控

- `GET /metrics`

## 8. 响应格式约定

### 成功

```json
{
  "code": "200",
  "message": "success",
  "data": {}
}
```

### 失败

```json
{
  "status": "error",
  "code": 40001,
  "message": "错误信息",
  "request_id": "uuid",
  "data": null
}
```

## 9. 开发规范（非常重要）

新增业务模块请遵循标准流程文档：

- [docs/add-module.md](docs/add-module.md)

简要流程：

1. 定义 `schema`
2. 定义 `model`（如需持久化）
3. 实现 `service`
4. 实现 `controller`
5. 注册 `blueprint`
6. 增加测试
7. 更新文档

## 10. 测试与质量检查

```bash
# 单测 + 覆盖率
.venv/bin/pytest -q

# Lint
.venv/bin/flake8 app tests

# 格式检查
.venv/bin/black --check app tests

# 类型检查
.venv/bin/mypy app
```

## 11. CI 流程

GitHub Actions 会执行：

1. 安装依赖
2. `flake8`
3. `black --check`
4. `mypy`
5. `pytest --cov-fail-under=60`
6. `docker build`

CI 文件：`.github/workflows/ci.yml`

## 12. 生产部署建议

- 使用 Postgres/MySQL，不建议生产使用 SQLite
- 限流存储切换到 Redis（当前默认 memory）
- 密钥通过 Secret 管理（不要写入仓库）
- 配置日志采集（ELK / Loki）
- 用 Prometheus + Grafana 监控接口延迟与错误率

## 13. Roadmap

- 提升关键路径覆盖率到 75%+
- 提供自动化模块脚手架
- 增加迁移治理文档（数据库变更策略）
- 增加版本发布与变更日志规范

Roadmap 细节见：

- [docs/template-roadmap.md](docs/template-roadmap.md)
- [docs/migration-governance.md](docs/migration-governance.md)
- [docs/release-policy.md](docs/release-policy.md)
- [docs/scaffold-module.md](docs/scaffold-module.md)
