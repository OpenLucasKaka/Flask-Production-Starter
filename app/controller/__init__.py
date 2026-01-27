from flask import Blueprint

auth_bp = Blueprint('auth',__name__)
message_bp = Blueprint('message',__name__)
health_bp = Blueprint('health',__name__)


from . import auth
from . import message
from . import health

