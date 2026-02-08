from app.controller import poster_bp
from app.exceptions.base import BusinessError
from app.services.poster import create_poster, search_poster
from app.utils.validators import (
    validate_json_content_type,
    login_required,
    validate_query,
)
from flask import g
from app.utils import success, error
from app.schemas.poster import Poster, ListUserQuery
from app.utils.validators import validate_request
from flask import request


@poster_bp.route("/add", methods=["POST"])
@validate_json_content_type()
@validate_request(Poster)
@login_required()
def add():
    try:
        data = g.validated_data
        result = create_poster(data)
        return success(result)
    except BusinessError as e:
        return error(code="400", message=str(e))
    except Exception as e:
        raise


@poster_bp.route("/list", methods=["GET"])
@validate_json_content_type()
@login_required()
@validate_query(ListUserQuery)
def list():
    try:
        data = g.query_data
        result = search_poster(page=data.page, page_size=data.page_size)
        return success(result)
    except BusinessError as e:
        raise BusinessError(code=400, message=str(e))
