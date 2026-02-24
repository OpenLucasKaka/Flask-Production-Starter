import pytest
from pydantic import ValidationError

from app.schemas.auth import ChangePassword, Login, RefreshToken, Register


def test_register_schema_accepts_valid_payload():
    payload = Register(
        username="demo_user",
        email="demo@example.com",
        password="StrongPass123",
    )
    assert payload.username == "demo_user"


def test_register_schema_rejects_bad_username():
    with pytest.raises(ValidationError):
        Register(
            username="demo user",
            email="demo@example.com",
            password="StrongPass123",
        )


def test_register_schema_rejects_weak_password():
    with pytest.raises(ValidationError):
        Register(
            username="demo_user",
            email="demo@example.com",
            password="weakpass",
        )


def test_login_schema_requires_identity():
    with pytest.raises(ValidationError):
        Login(password="StrongPass123")


def test_login_schema_accepts_username_or_email():
    by_username = Login(username="demo", password="StrongPass123")
    by_email = Login(email="demo@example.com", password="StrongPass123")
    assert by_username.username == "demo"
    assert by_email.email == "demo@example.com"


def test_change_password_schema_rejects_weak_password():
    with pytest.raises(ValidationError):
        ChangePassword(old_password="OldPass123", new_password="nopattern")


def test_refresh_token_schema():
    payload = RefreshToken(refresh_token="token")
    assert payload.refresh_token == "token"
