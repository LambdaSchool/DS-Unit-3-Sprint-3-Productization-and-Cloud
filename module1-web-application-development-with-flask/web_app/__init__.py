from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes
from web_app.routes.user_routes import user_routes
from web_app.models import db, migrate


DATABASE_URI = "sqlite:///test_db.db"


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(user_routes)
    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)