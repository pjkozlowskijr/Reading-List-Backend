from flask_login import login_required
from . import bp as api
from app.models import Book
from flask import make_response, request, abort
from app.blueprints.auth.auth import token_auth
from helpers import require_admin

@api.get("/book")
def get_books():
    books = Book.query.all()
    books = [book.to_dict() for book in books]
    return make_response({"book": books}, 200)

@api.get("/book/<int:id>")
def get_book(id):
    book = Book.query.get(id)
    if not book:
        abort(404)
    return make_response(book.to_dict(), 200)

@api.post("/book")
@token_auth.login_required()
@require_admin
def post_book():
    book_dict = request.get_json()
    if not all(key in book_dict for key in ("title", "author", "subject", "summary", "pages", "image")):
        abort(400)
    book = Book()
    book.from_dict(book_dict)
    book.save()
    return make_response(f"Book {book.name} was created with ID {book.id}.", 200)

@api.put("/book/<int:id>")
@token_auth.login_required()
@require_admin
def put_book(id):
    book_dict = request.get_json()
    book = Book.query.get(id)
    if not book:
        abort(404)
    book.from_dict(book_dict)
    book.save()
    return make_response(f"Book {book.name} with ID {book.id} has been updated.", 200)

@api.delete("/book/<ind:id>")
@token_auth.login_required()
@require_admin
def delete_book(id):
    book_to_delete = Book.query.get(id)
    if not book_to_delete:
        abort(404)
    book_to_delete.delete()
    return make_response(f"Book with ID {id} has been deleted.", 200)
