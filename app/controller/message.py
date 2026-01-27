from flask import request

from app.controller import message_bp

@message_bp.route('/message', methods = ['GET'])
def find_post(data):
    page = request.args.get('page',1)
    page_size = request.args.get('page_size',10)


