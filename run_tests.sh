#!/usr/bin/env bash
# 运行单元测试的脚本

echo "======================================="
echo "开始运行单元测试"
echo "======================================="

# 运行测试
pytest -v \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    tests/

echo ""
echo "======================================="
echo "测试完成！"
echo "HTML 覆盖率报告: htmlcov/index.html"
echo "======================================="
