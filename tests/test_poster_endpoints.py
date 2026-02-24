from types import SimpleNamespace

from flask_jwt_extended import create_access_token

from app.models.user import User
from app.services.auth_service import register_user


def _auth_headers(app, username="poster_user", email="poster@example.com"):
    with app.app_context():
        register_user(
            SimpleNamespace(username=username, email=email, password="StrongPass123")
        )
        user = User.query.filter_by(username=username).first()
        token = create_access_token(identity=str(user.user_id))
    return {"Authorization": f"Bearer {token}"}


def test_poster_crud_flow(client, app, db_init):
    headers = _auth_headers(app)

    create_resp = client.post(
        "/poster/add",
        json={"title": "poster01", "content": "content01", "status": 256},
        headers=headers,
    )
    assert create_resp.status_code == 200
    poster_id = create_resp.json["data"]["id"]

    list_resp = client.get("/poster/list?page=1&page_size=10", headers=headers)
    assert list_resp.status_code == 200
    assert list_resp.json["data"]["total"] >= 1

    detail_resp = client.get(f"/poster/{poster_id}", headers=headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json["data"]["id"] == poster_id

    update_resp = client.put(
        f"/poster/{poster_id}",
        json={"title": "poster02", "content": "updated"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json["data"]["title"] == "poster02"

    delete_resp = client.delete(f"/poster/{poster_id}", headers=headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json["data"]["deleted"] is True

    deleted_detail = client.get(f"/poster/{poster_id}", headers=headers)
    assert deleted_detail.status_code == 404


def test_poster_endpoints_require_auth(client, db_init):
    resp = client.get("/poster/list?page=1&page_size=10")
    assert resp.status_code == 403


def test_public_message_list_only_returns_published(client, app, db_init):
    headers = _auth_headers(app, username="public_user", email="public@example.com")

    client.post(
        "/poster/add",
        json={"title": "draft01", "content": "draft", "status": 4},
        headers=headers,
    )
    client.post(
        "/poster/add",
        json={"title": "pub01xx", "content": "public", "status": 256},
        headers=headers,
    )

    resp = client.get("/message?page=1&page_size=10")
    assert resp.status_code == 200
    assert resp.json["data"]["total"] >= 1
    assert all(item["status"] == 256 for item in resp.json["data"]["list"])
