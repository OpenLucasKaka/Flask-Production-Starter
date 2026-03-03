"""
系统级自检（System Checks）
用于企业模板的启动前检查、readiness 检查和运维巡检。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from flask import current_app
from sqlalchemy import text

from app.extensions.extensions import db


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


def _check_database_connection() -> CheckResult:
    try:
        db.session.execute(text("SELECT 1"))
        return CheckResult("database_connection", "pass", "database connected")
    except Exception as exc:
        db.session.rollback()
        return CheckResult("database_connection", "fail", str(exc))


def _check_required_production_secrets() -> CheckResult:
    env = (
        current_app.config.get("APP_ENV")
        or current_app.config.get("ENV")
        or "development"
    ).lower()
    if env != "production":
        return CheckResult("required_secrets", "pass", "not required in non-production")

    required = ("SECRET_KEY", "JWT_SECRET_KEY", "SQLALCHEMY_DATABASE_URI")
    missing = [key for key in required if not current_app.config.get(key)]
    if missing:
        return CheckResult(
            "required_secrets",
            "fail",
            f"missing required config: {', '.join(missing)}",
        )
    return CheckResult("required_secrets", "pass", "all required config present")


def _check_rate_limit_storage() -> CheckResult:
    env = (
        current_app.config.get("APP_ENV")
        or current_app.config.get("ENV")
        or "development"
    ).lower()
    storage_uri = current_app.config.get("RATE_LIMIT_STORAGE_URI", "memory://")
    if env == "production" and str(storage_uri).startswith("memory://"):
        return CheckResult(
            "rate_limit_storage",
            "warn",
            "memory:// detected in production, recommend redis:// for multi-instance",
        )
    return CheckResult("rate_limit_storage", "pass", f"storage={storage_uri}")


def _check_sqlalchemy_pool() -> CheckResult:
    options = current_app.config.get("SQLALCHEMY_ENGINE_OPTIONS") or {}
    pool_size = options.get("pool_size")
    max_overflow = options.get("max_overflow")
    if pool_size is None or max_overflow is None:
        return CheckResult(
            "sqlalchemy_pool",
            "warn",
            "pool_size/max_overflow missing in SQLALCHEMY_ENGINE_OPTIONS",
        )
    return CheckResult(
        "sqlalchemy_pool",
        "pass",
        f"pool_size={pool_size}, max_overflow={max_overflow}",
    )


def run_system_checks() -> dict[str, Any]:
    checks = [
        _check_database_connection(),
        _check_required_production_secrets(),
        _check_rate_limit_storage(),
        _check_sqlalchemy_pool(),
    ]

    summary = {"pass": 0, "warn": 0, "fail": 0}
    for check in checks:
        summary[check.status] += 1

    overall = (
        "fail" if summary["fail"] > 0 else "degraded" if summary["warn"] > 0 else "pass"
    )
    return {
        "status": overall,
        "summary": summary,
        "checks": [item.to_dict() for item in checks],
    }
