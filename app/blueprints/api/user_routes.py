from lib2to3.pgen2 import token
from flask_login import login_required
from . import bp as api
from app.models import User
from flask import make_response, request, abort, g
from app.blueprints.auth.auth import token_auth
from helpers import require_admin

@api.post("/user")
def post_user():
    user_dict = request.get_json()
    if not all(key in user_dict for key in ("first_name", "last_name", "email", "password")):
        abort(400)
    user = User()
    user.from_dict(user_dict)
    user.save()
    return make_response(f"User {user.first_name} {user.last_name} was created with ID {user.id}.", 200)

@api.put("/user/<int:id>")
@token_auth.login_required()
def put_user(id):
    user_dict = request.get_json()
    user = User.query.get(id)
    if not user:
        abort(404)
    if not user.id == g.current_user.id:
        abort(403)
    user.from_dict(user_dict)
    user.save()
    return make_response(f"User {user.first_name} {user.last_name} with ID {user.id} has been updated.", 200)

@api.delete("/user/<ind:id>")
@token_auth.login_required()
def delete_user(id):
    user_to_delete = User.query.get(id)
    if not user_to_delete:
        abort(404)
    if not user_to_delete.id == g.current_user.id:
        abort(403)
    user_to_delete.delete()
    return make_response(f"User with ID {user.id} has been deleted.", 200)