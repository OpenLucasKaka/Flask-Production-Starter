# Enterprise Template Standard

本文档定义该 Flask 模板作为企业项目脚手架时的最低技术基线。

## 1. 运行时标准

1. `GET /health`：仅用于 liveness，检查进程是否可响应。
2. `GET /readiness`：用于 readiness，失败返回 `503`。
3. `GET /ops/system-checks`：返回系统自检详情（pass/warn/fail）。
4. `flask system-check`：部署前必须执行，`fail` 状态必须阻断发布。

## 2. 配置治理标准

1. 生产环境必须设置：
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
   - `DATABASE_URL`
2. 生产环境不得使用 `memory://` 作为限流存储（应改为 Redis）。
3. 数据库连接池参数必须显式配置：`pool_size` / `max_overflow`。
4. 所有配置必须通过环境变量注入，不得硬编码密钥。

## 3. 质量门禁标准

本仓库统一命令：

```bash
make quality      # black --check + flake8 + mypy
make test         # pytest
make system-check # flask system-check
make ci           # quality + test + system-check
```

CI 必须阻断以下问题：

1. 代码风格不一致
2. 静态检查失败
3. 单元测试失败
4. 系统自检失败

## 4. 可观测性标准

1. 请求追踪：`X-Request-ID`
2. 响应耗时：`X-Response-Time`
3. Prometheus 指标：`/metrics`
4. 结构化日志（生产环境 JSON）

## 5. 模板扩展建议（下一阶段）

1. 审计日志（操作人、资源、动作、结果）
2. OpenTelemetry Trace/Metric/Log 全链路
3. SAST/Dependency Scan（如 Bandit、pip-audit、Trivy）
4. 数据库迁移自动检查（Alembic drift detection）
5. 多环境配置分层（dev/staging/prod + secret manager）
