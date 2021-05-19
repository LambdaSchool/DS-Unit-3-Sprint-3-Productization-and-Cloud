# web_app/routes/users_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect

from web_app.models import Users, db

users_routes = Blueprint("users_routes", __name__)

@users_routes.route("/users.json")
@users_routes.route("/users_endpoint")
def list_users():
    users = [
        {"id": 1, "handle": "@elonmusk"},
        {"id": 2, "handle": "@kobebryant"},
        {"id": 3, "handle": "@neiltyson"},
    ]
    return jsonify(users)

@users_routes.route("/users")
def list_users_for_humans():
    #users = [
    #    {"id": 1, "handle": "@elonmusk"},
        # {"id": 2, "handle": "@kobebryant"},
        # {"id": 3, "handle": "@neiltyson"},
    #]

    users_records = Users.query.all()
    print(users_records)

    return render_template("users.html", message="Here's some users", users=users_records)

@users_routes.route("/users/new")
def new_user():
    return render_template("new_user.html")

@users_routes.route("/users/create", methods=["POST"])
def create_user():
    print("FORM DATA:", dict(request.form))

    new_user = Users(handle=request.form["handle"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "USER CREATED OK",
        "user": dict(request.form)
    })
    #flash(f"Book '{new_book.title}' created successfully!", "success")
    #return redirect("/books")