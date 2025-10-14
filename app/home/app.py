"""
lakeblvd.net homepage
"""
from flask import Blueprint, render_template

bp = Blueprint('home', __name__, template_folder='templates')

@bp.route('/', methods=["GET", "POST"])
def index():
    return render_template("home/index.html")

@bp.route('/about', methods=["GET", "POST"])
def about():
    return render_template("home/about.html")