from app.models.poster import Poster


def list_messages(page: int = 1, page_size: int = 10):
    pagination = (
        Poster.query.filter(Poster.status == 256)
        .order_by(Poster.id.desc())
        .paginate(
            page=max(page, 1),
            per_page=min(max(page_size, 1), 100),
            error_out=False,
        )
    )
    return {
        "list": [item.to_dict() for item in pagination.items],
        "page": pagination.page,
        "page_size": pagination.per_page,
        "total": pagination.total,
    }
