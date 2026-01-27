# gunicorn.conf.py

import multiprocessing

# 绑定地址和端口
bind = "0.0.0.0:8000"

# worker 数量：CPU * 2 + 1（经典公式）
workers = multiprocessing.cpu_count() * 2 + 1

# worker 类型
worker_class = "sync"

# 请求超时时间（秒）
timeout = 30

# 是否后台运行（Docker 中必须 False）
daemon = False

# 日志级别
loglevel = "info"

# 访问日志（stdout，方便 docker logs）
accesslog = "-"

# 错误日志（stderr）
errorlog = "-"
