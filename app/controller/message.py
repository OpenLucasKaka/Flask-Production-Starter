from flask import request
from app.controller import message_bp
from app.utils import success


@message_bp.route("/message", methods=["GET"])
def find_post():
    page = request.args.get("page", 1)
    page_size = request.args.get("page_size", 10)
    return success({"page": int(page), "page_size": int(page_size)})
