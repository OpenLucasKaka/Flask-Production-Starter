"""
健康检查和就绪检查端点
- /health: 基本健康状态
- /readiness: 详细的就绪检查（包括数据库连接）
"""

from flask import jsonify
from app.controller import health_bp
from app.extensions.system_checks import run_system_checks


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    基本健康检查
    - 应用正在运行返回 200
    - 用于 k8s liveness probe
    """
    return jsonify({"status": "healthy", "message": "Application is running"}), 200


@health_bp.route("/readiness", methods=["GET"])
def readiness_check():
    """
    就绪检查 - 检查关键依赖
    - 数据库连接是否正常
    - 用于 k8s readiness probe
    """
    report = run_system_checks()
    if report["status"] == "fail":
        return jsonify({"status": "not_ready", "checks": report["checks"]}), 503
    return jsonify({"status": "ready", "checks": report["checks"]}), 200


@health_bp.route("/ops/system-checks", methods=["GET"])
def system_checks():
    """
    系统巡检端点
    - pass: 全部通过
    - degraded: 存在告警（warn）
    - fail: 存在失败项
    """
    report = run_system_checks()
    http_code = 500 if report["status"] == "fail" else 200
    return jsonify(report), http_code
