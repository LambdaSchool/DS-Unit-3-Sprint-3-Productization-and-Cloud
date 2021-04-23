from flask import Flask

app = Flask(__name__)

from app import aq_dashboard


app.run(debug=True)
