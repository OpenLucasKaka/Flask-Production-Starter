import os

import pytest

from app.utils.env_validator import EnvironmentValidator


def test_set_defaults_sets_missing_values(monkeypatch):
    monkeypatch.delenv("FLASK_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    EnvironmentValidator.set_defaults()

    assert os.getenv("FLASK_ENV") == "development"
    assert os.getenv("LOG_LEVEL") == "INFO"


def test_validate_returns_true_in_development(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "development")
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    assert EnvironmentValidator.validate() is True


def test_validate_raises_when_production_secrets_missing(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(EnvironmentError):
        EnvironmentValidator.validate()
