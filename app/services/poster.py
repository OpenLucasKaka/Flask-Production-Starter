from app.exceptions.base import BusinessError
from app.models import Poster
from app.extensions.extensions import db
from flask import g
from app.utils.pagination import pagination


def create_poster(data):
    content = data.content.strip()
    title = data.title.strip()
    status = data.status
    user_id = g.user_id
    if not content:
        raise BusinessError("内容不能为空", code=400)
    if not title:
        raise BusinessError("标题不能为空", code=400)
    if status not in (4, 256):
        raise BusinessError("状态错误", code=400)
    poster = Poster(content=content, title=title, status=status, user_id=user_id)
    try:
        db.session.add(poster)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise BusinessError("新增失败", code=500)
    return {"id": poster.id}


def search_poster(page: int = 1, page_size: int = 10):
    """
    分页查询 Poster
    """

    # 1️⃣ 参数兜底（防止恶意请求）
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)

    try:
        pagination = Poster.query.paginate(
            page=page, per_page=page_size, error_out=False
        )

    except Exception as e:
        raise BusinessError("查询失败", code=500)
    items = [p.to_dict() for p in pagination.items]

    # 3️⃣ 返回“干净”的业务数据
    return {
        "list": items,
        "page": page,
        "page_size": page_size,
        "total": pagination.total,
    }
