#!/usr/bin/env python3
"""测试 Flask 应用的 health 端点"""
import time
import subprocess
import requests
import signal
import os

# 启动 Flask 应用
print("启动 Flask 应用...")
process = subprocess.Popen(
    ["/Users/weiluo/.local/bin/uv", "run", "flask", "run", "--port=5555"],
    cwd="/Users/weiluo/open/flask_py"
)

try:
    # 等待应用启动
    time.sleep(3)
    
    # 测试端点
    print("测试 /health 端点...")
    response = requests.get("http://127.0.0.1:5555/health", timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print(f"JSON: {response.json()}")
    
except Exception as e:
    print(f"错误: {e}")
finally:
    # 关闭 Flask 应用
    print("\n关闭 Flask 应用...")
    process.terminate()
    process.wait(timeout=5)
