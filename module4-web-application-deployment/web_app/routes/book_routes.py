
from flask import Blueprint, jsonify, request, render_template, redirect, flash
from pdb import set_trace as st
from web_app.models import Book, db

book_routes = Blueprint("book_routes", __name__)


@book_routes.route("/books.json")
def list_books_json():
    book_records = Book.query.all()
    return jsonify(book_records)


@book_routes.route("/books")
def list_books():
    book_records = Book.query.all()
    return render_template("books.html", message="Here's some books", books=book_records)


@book_routes.route("/books/new")
def new_book():
    return render_template("new_book.html")


@book_routes.route("/books/create", methods=["POST"])
def create_book():
    print("FORM DATA:", dict(request.form))
    new_book = Book(title=request.form["book_title"], author_id=request.form["author_name"])

    db.session.add(new_book)
    db.session.commit()
    return redirect(f"/books")