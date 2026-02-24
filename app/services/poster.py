from app.exceptions.base import BusinessError
from app.models import Poster
from app.models.user import User
from app.extensions.extensions import db
from flask import g


def _require_current_user():
    user_identity = g.get("user_id")
    user = User.query.filter(User.user_id == user_identity).first()
    if not user:
        raise BusinessError("用户不存在", code=40004, http_code=404)
    return user


def create_poster(data):
    content = data.content.strip()
    title = data.title.strip()
    status = data.status
    user = _require_current_user()
    if not content:
        raise BusinessError("内容不能为空", code=40002, http_code=400)
    if not title:
        raise BusinessError("标题不能为空", code=40002, http_code=400)
    if status not in (4, 256):
        raise BusinessError("状态错误", code=40002, http_code=400)
    poster = Poster(content=content, title=title, status=status, user_id=user.id)
    try:
        db.session.add(poster)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise BusinessError("新增失败", code=50001, http_code=500)
    return {"id": poster.id}


def search_poster(page: int = 1, page_size: int = 10, status: int | None = None):
    user = _require_current_user()
    try:
        query = Poster.query.filter(Poster.user_id == user.id).order_by(
            Poster.id.desc()
        )
        if status is not None:
            query = query.filter(Poster.status == status)

        pagination = query.paginate(
            page=max(page, 1), per_page=min(max(page_size, 1), 100), error_out=False
        )
    except Exception:
        raise BusinessError("查询失败", code=50001, http_code=500)
    items = [p.to_dict() for p in pagination.items]

    return {
        "list": items,
        "page": pagination.page,
        "page_size": pagination.per_page,
        "total": pagination.total,
    }


def get_poster_detail(poster_id: int):
    user = _require_current_user()
    poster = Poster.query.filter(
        Poster.id == poster_id, Poster.user_id == user.id
    ).first()
    if not poster:
        raise BusinessError("帖子不存在", code=40401, http_code=404)
    return poster.to_dict()


def update_poster(poster_id: int, data):
    user = _require_current_user()
    poster = Poster.query.filter(
        Poster.id == poster_id, Poster.user_id == user.id
    ).first()
    if not poster:
        raise BusinessError("帖子不存在", code=40401, http_code=404)

    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise BusinessError("至少提供一个更新字段", code=40002, http_code=400)

    if "status" in payload and payload["status"] not in (4, 256):
        raise BusinessError("状态错误", code=40002, http_code=400)

    if "title" in payload:
        poster.title = payload["title"].strip()
    if "content" in payload:
        poster.content = payload["content"].strip()
    if "status" in payload:
        poster.status = payload["status"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise BusinessError("更新失败", code=50001, http_code=500)
    return poster.to_dict()


def delete_poster(poster_id: int):
    user = _require_current_user()
    poster = Poster.query.filter(
        Poster.id == poster_id, Poster.user_id == user.id
    ).first()
    if not poster:
        raise BusinessError("帖子不存在", code=40401, http_code=404)
    try:
        db.session.delete(poster)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise BusinessError("删除失败", code=50001, http_code=500)
    return {"id": poster_id, "deleted": True}
