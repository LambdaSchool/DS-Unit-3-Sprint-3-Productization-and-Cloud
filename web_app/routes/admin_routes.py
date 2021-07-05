# web_app/routes/admin_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect

from web_app.models import db
from web_app.routes.twitter_routes import store_twitter_user_data

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route("/admin/db/reset")
def reset_db():
    print(type(db))
    db.drop_all()
    db.create_all()
    return jsonify({"message": "DB RESET OK"})


@admin_routes.route("/admin/db/seed")
def seed_db():
    print(type(db))
    default_users = ["elonmusk", "justinbieber", "s2t2", "austen", "nbcnews"]
    for screen_name in default_users:
        db_user, statuses = store_twitter_user_data(screen_name)

    return jsonify({"message": f"DB SEEDED OK (w/ {len(default_users)})"})
