from types import SimpleNamespace

import pytest
from flask import Flask, g
from flask_jwt_extended import JWTManager

from app.exceptions.base import BusinessError
from app.extensions.extensions import bcrypt, db
from app.models.poster import Poster
from app.models.user import Refresh, User
from app.services.auth_service import is_user, register_user, user_login, user_profile
from app.services.auth_service import rotate_refresh_token, revoke_refresh_token
from app.services.poster import create_poster, search_poster


@pytest.fixture(scope="function")
def service_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test-secret"
    app.config["JWT_SECRET_KEY"] = "jwt-test-secret"

    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def _register_data(username="demo", email="demo@example.com", password="Strong123A"):
    return SimpleNamespace(username=username, email=email, password=password)


def test_register_user_success(service_app):
    with service_app.app_context():
        result = register_user(_register_data())
        user = User.query.filter_by(username="demo").first()
        assert result["username"] == "demo"
        assert user is not None
        assert user.password != "Strong123A"


def test_register_user_duplicate_raises_value_error(service_app):
    with service_app.app_context():
        register_user(_register_data())
        with pytest.raises(ValueError):
            register_user(_register_data())


def test_user_login_success_creates_refresh_record(service_app):
    with service_app.app_context():
        register_user(_register_data())
        data = user_login("demo@example.com", "demo", "Strong123A")
        refresh_record = Refresh.query.first()
        assert "token" in data
        assert "refresh" in data
        assert refresh_record is not None
        assert refresh_record.is_revoked is False


def test_user_login_wrong_password_raises_business_error(service_app):
    with service_app.app_context():
        register_user(_register_data())
        with pytest.raises(BusinessError) as exc:
            user_login("demo@example.com", "demo", "WrongPass123")
        assert exc.value.code == 40005


def test_user_profile_not_found_raises_business_error(service_app):
    with service_app.app_context():
        with pytest.raises(BusinessError):
            user_profile(123)


def test_is_user_refreshes_access_token(service_app, monkeypatch):
    with service_app.app_context():
        register_user(_register_data())
        user = User.query.filter_by(username="demo").first()
        monkeypatch.setattr(
            "app.services.auth_service.get_jwt_identity", lambda: user.user_id
        )
        result = is_user()
        assert "access_token" in result


def test_rotate_refresh_token_rotates_and_revokes_previous(service_app, monkeypatch):
    with service_app.app_context():
        register_user(_register_data())
        user = User.query.filter_by(username="demo").first()
        login_data = user_login("demo@example.com", "demo", "Strong123A")
        monkeypatch.setattr(
            "app.services.auth_service.get_jwt_identity", lambda: str(user.user_id)
        )

        result = rotate_refresh_token(login_data["refresh"])
        records = Refresh.query.filter_by(user_id=user.id).all()

        assert "access_token" in result
        assert "refresh_token" in result
        assert len(records) == 2
        assert any(r.is_revoked for r in records)
        assert any(not r.is_revoked for r in records)


def test_revoke_refresh_token_marks_token_revoked(service_app, monkeypatch):
    with service_app.app_context():
        register_user(_register_data())
        user = User.query.filter_by(username="demo").first()
        login_data = user_login("demo@example.com", "demo", "Strong123A")
        monkeypatch.setattr(
            "app.services.auth_service.get_jwt_identity", lambda: str(user.user_id)
        )

        result = revoke_refresh_token(login_data["refresh"])
        record = Refresh.query.filter_by(user_id=user.id).first()

        assert result["revoked"] is True
        assert record.is_revoked is True


def test_create_poster_success(service_app):
    with service_app.app_context():
        register_user(_register_data())
        user = User.query.filter_by(username="demo").first()
        with service_app.test_request_context("/poster/add", method="POST"):
            g.user_id = user.user_id
            result = create_poster(
                SimpleNamespace(title="hello", content="world", status=4)
            )
            assert "id" in result
            assert Poster.query.count() == 1


def test_create_poster_rejects_invalid_status(service_app):
    with service_app.app_context():
        register_user(_register_data())
        user = User.query.filter_by(username="demo").first()
        with service_app.test_request_context("/poster/add", method="POST"):
            g.user_id = user.user_id
            with pytest.raises(BusinessError):
                create_poster(SimpleNamespace(title="hello", content="world", status=1))


def test_search_poster_paginated(service_app):
    with service_app.app_context():
        register_user(_register_data())
        user = User.query.filter_by(username="demo").first()
        for idx in range(3):
            db.session.add(
                Poster(
                    title=f"title-{idx}",
                    content="content",
                    status=4,
                    user_id=user.id,
                )
            )
        db.session.commit()

        with service_app.test_request_context("/poster/list", method="GET"):
            g.user_id = user.user_id
            result = search_poster(page=1, page_size=2)
            assert result["page"] == 1
            assert result["page_size"] == 2
            assert result["total"] == 3
            assert len(result["list"]) == 2
