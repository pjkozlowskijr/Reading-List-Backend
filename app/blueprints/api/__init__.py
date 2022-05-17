from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

from . import auth_routes, book_routes, user_routes