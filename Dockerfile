# ===============================
# 构建阶段
# ===============================
FROM python:3.11-slim AS build

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 拷贝项目文件
COPY . .

# 升级 pip 并安装依赖
RUN pip install --upgrade pip && pip install .


# ===============================
# 生产阶段：干净镜像
# ===============================
FROM python:3.11-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 只拷贝虚拟环境，不需要构建工具
COPY --from=build /opt/venv /opt/venv

# 拷贝项目代码
COPY . .

# 添加虚拟环境到 PATH
ENV PATH="/opt/venv/bin:$PATH"

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
