"""
示例业务模块：帖子相关 API 端点
"""

from app.controller import poster_bp
from app.services.poster import (
    create_poster,
    delete_poster,
    get_poster_detail,
    search_poster,
    update_poster,
)
from app.utils.validators import (
    validate_json_content_type,
    login_required,
    validate_query,
)
from flask import g
from app.utils import success
from app.schemas.poster import PosterCreate, PosterUpdate, ListPosterQuery
from app.utils.validators import validate_request


@poster_bp.route("/add", methods=["POST"])
@validate_json_content_type()
@validate_request(PosterCreate)
@login_required()
def add():
    data = g.validated_data
    result = create_poster(data)
    return success(result)


@poster_bp.route("/list", methods=["GET"])
@login_required()
@validate_query(ListPosterQuery)
def list():
    data = g.query_data
    result = search_poster(page=data.page, page_size=data.page_size, status=data.status)
    return success(result)


@poster_bp.route("/<int:poster_id>", methods=["GET"])
@login_required()
def detail(poster_id):
    result = get_poster_detail(poster_id)
    return success(result)


@poster_bp.route("/<int:poster_id>", methods=["PUT"])
@validate_json_content_type()
@validate_request(PosterUpdate)
@login_required()
def update(poster_id):
    data = g.validated_data
    result = update_poster(poster_id, data)
    return success(result)


@poster_bp.route("/<int:poster_id>", methods=["DELETE"])
@login_required()
def delete(poster_id):
    result = delete_poster(poster_id)
    return success(result)
