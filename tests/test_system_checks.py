from app.extensions.system_checks import run_system_checks


def test_ops_system_checks_endpoint_returns_report(client):
    response = client.get("/ops/system-checks")
    assert response.status_code == 200
    body = response.get_json()
    assert "status" in body
    assert "summary" in body
    assert "checks" in body
    assert isinstance(body["checks"], list)


def test_readiness_returns_503_when_system_check_failed(client, monkeypatch):
    monkeypatch.setattr(
        "app.controller.health.run_system_checks",
        lambda: {
            "status": "fail",
            "summary": {"pass": 0, "warn": 0, "fail": 1},
            "checks": [
                {"name": "database_connection", "status": "fail", "detail": "down"}
            ],
        },
    )
    response = client.get("/readiness")
    assert response.status_code == 503
    assert response.get_json()["status"] == "not_ready"


def test_system_check_cli_success(runner, monkeypatch):
    monkeypatch.setattr(
        "app.run_system_checks",
        lambda: {
            "status": "pass",
            "summary": {"pass": 4, "warn": 0, "fail": 0},
            "checks": [],
        },
    )
    result = runner.invoke(args=["system-check"])
    assert result.exit_code == 0
    assert "status=pass" in result.output


def test_system_checks_warn_for_memory_rate_limit_in_production(app):
    with app.app_context():
        app.config["APP_ENV"] = "production"
        app.config["RATE_LIMIT_STORAGE_URI"] = "memory://"
        app.config["SECRET_KEY"] = "secret"
        app.config["JWT_SECRET_KEY"] = "jwt-secret"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        report = run_system_checks()

    by_name = {item["name"]: item for item in report["checks"]}
    assert by_name["rate_limit_storage"]["status"] == "warn"
