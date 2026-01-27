from flask import jsonify
from flask import Response
import json

def success(data,message='success', http_code=200,code='200'):
    return Response(
        json.dumps({ "code": code,
        "message": message,
        "data": data}, ensure_ascii=False),
        mimetype="application/json"
    ), http_code

def error(code, message='error', http_code=400):
    return jsonify({
        "code": code,
        "message": message,
        "data": None
    }), http_code



