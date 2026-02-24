from flask import g

from app.controller import message_bp
from app.schemas.poster import ListPosterQuery
from app.services.message_service import list_messages
from app.utils import success
from app.utils.validators import validate_query


@message_bp.route("/message", methods=["GET"])
@validate_query(ListPosterQuery)
def find_post():
    data = g.query_data
    return success(list_messages(page=data.page, page_size=data.page_size))
