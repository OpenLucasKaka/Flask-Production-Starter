#!/bin/bash
set -e

echo "启动 Flask 应用..."
cd /Users/weiluo/open/flask_py
/Users/weiluo/.local/bin/uv run flask run --port=5555 > /tmp/flask.log 2>&1 &
FLASK_PID=$!

echo "Flask PID: $FLASK_PID"
echo "等待应用启动..."
sleep 4

echo "测试 /health 端点..."
if curl -s http://127.0.0.1:5555/health; then
    echo ""
    echo "✓ 端点响应成功"
else
    echo ""
    echo "✗ 端点无响应"
    echo "Flask 日志:"
    cat /tmp/flask.log
fi

echo "关闭 Flask..."
kill $FLASK_PID 2>/dev/null || true
wait $FLASK_PID 2>/dev/null || true
