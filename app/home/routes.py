"""
lakeblvd.net homepage
"""
from flask import Flask, render_template, url_for
from ..extensions import db
from config import section
from ..auth.forms import LoginForm

def create_app():
    app = Flask(__name__)
    SECRET_KEY = section("App")['SECRET_KEY']
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///lakeblvd-home.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app = create_app()

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")
