import pytest
from flask import Flask, g
from flask_jwt_extended.exceptions import NoAuthorizationError
from pydantic import BaseModel

from app.exceptions.base import AuthorizationError, BusinessError, QueryError
from app.utils.validators import (
    login_required,
    permission_required,
    validate_json_content_type,
    validate_query,
    validate_request,
)


class DummySchema:
    def __init__(self, **kwargs):
        if kwargs.get("raise_error"):
            raise ValueError("invalid payload")
        self.value = kwargs.get("value")


class QuerySchema(BaseModel):
    page: int


def _make_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


def test_validate_request_success():
    app = _make_app()

    @validate_request(DummySchema)
    def handler():
        return g.validated_data.value

    with app.test_request_context("/", method="POST", json={"value": 1}):
        assert handler() == 1


def test_validate_request_missing_json():
    app = _make_app()

    @validate_request(DummySchema)
    def handler():
        return "ok"

    with app.test_request_context(
        "/", method="POST", data="null", content_type="application/json"
    ):
        with pytest.raises(BusinessError):
            handler()


def test_validate_json_content_type_rejects_non_json():
    app = _make_app()

    @validate_json_content_type()
    def handler():
        return "ok"

    with app.test_request_context("/", method="POST", content_type="text/plain"):
        with pytest.raises(BusinessError):
            handler()


def test_validate_query_success():
    app = _make_app()

    @validate_query(DummySchema)
    def handler():
        return g.query_data.value

    with app.test_request_context("/?value=2", method="GET"):
        assert handler() == "2"


def test_validate_query_error():
    app = _make_app()

    @validate_query(QuerySchema)
    def handler():
        return "ok"

    with app.test_request_context("/?page=oops", method="GET"):
        with pytest.raises(QueryError):
            handler()


def test_login_required_success(monkeypatch):
    app = _make_app()

    monkeypatch.setattr("app.utils.validators.verify_jwt_in_request", lambda: None)
    monkeypatch.setattr("app.utils.validators.get_jwt_identity", lambda: "u-1")

    @login_required()
    def handler():
        return g.user_id

    with app.test_request_context("/", method="GET"):
        assert handler() == "u-1"


def test_login_required_no_auth(monkeypatch):
    app = _make_app()

    def _raise_auth():
        raise NoAuthorizationError("missing")

    monkeypatch.setattr("app.utils.validators.verify_jwt_in_request", _raise_auth)

    @login_required()
    def handler():
        return "ok"

    with app.test_request_context("/", method="GET"):
        with pytest.raises(AuthorizationError):
            handler()


def test_permission_required_user_not_found(monkeypatch):
    app = _make_app()

    class DummyUser:
        class query:
            @staticmethod
            def get(_):
                return None

    monkeypatch.setattr("app.utils.validators.get_jwt_identity", lambda: 1)
    monkeypatch.setattr("app.utils.validators.User", DummyUser)

    @permission_required("manage")
    def handler():
        return "ok"

    with app.test_request_context("/", method="GET"):
        response, status = handler()
        assert status == 404


def test_permission_required_forbidden(monkeypatch):
    app = _make_app()

    class Perm:
        def __init__(self, code):
            self.code = code

    class Role:
        def __init__(self, permissions):
            self.permissions = permissions

    class UserObj:
        roles = [Role([Perm("read")])]

    class DummyUser:
        class query:
            @staticmethod
            def get(_):
                return UserObj()

    monkeypatch.setattr("app.utils.validators.get_jwt_identity", lambda: 1)
    monkeypatch.setattr("app.utils.validators.User", DummyUser)

    @permission_required("manage")
    def handler():
        return "ok"

    with app.test_request_context("/", method="GET"):
        response, status = handler()
        assert status == 403


def test_permission_required_success(monkeypatch):
    app = _make_app()

    class Perm:
        def __init__(self, code):
            self.code = code

    class Role:
        def __init__(self, permissions):
            self.permissions = permissions

    class UserObj:
        roles = [Role([Perm("manage")])]

    class DummyUser:
        class query:
            @staticmethod
            def get(_):
                return UserObj()

    monkeypatch.setattr("app.utils.validators.get_jwt_identity", lambda: 1)
    monkeypatch.setattr("app.utils.validators.User", DummyUser)

    @permission_required("manage")
    def handler():
        return "ok"

    with app.test_request_context("/", method="GET"):
        assert handler() == "ok"
