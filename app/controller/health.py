"""
健康检查和就绪检查端点
- /health: 基本健康状态
- /readiness: 详细的就绪检查（包括数据库连接）
"""

from flask import jsonify
from sqlalchemy import text
from app.extensions.extensions import db
from app.controller import health_bp


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
    try:
        # 测试数据库连接
        db.session.execute(text("SELECT 1"))

        return (
            jsonify(
                {
                    "status": "ready",
                    "message": "Application is ready to serve traffic",
                    "database": "connected",
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "status": "not_ready",
                    "message": "Application is not ready",
                    "error": str(e),
                    "database": "disconnected",
                }
            ),
            503,
        )
