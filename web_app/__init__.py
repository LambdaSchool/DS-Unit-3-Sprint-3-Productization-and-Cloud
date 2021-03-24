# what init is for
# entry point into a specifiy directory 
# first place python will look for files
from flask import Flask

from web_app.routes.home_routes import home_routes
#from web_app.routes.book_routes import book_routes

# application factory pattern
def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_routes)
    #app.register_blueprint(book_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)