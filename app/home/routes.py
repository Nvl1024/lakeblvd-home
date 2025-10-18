"""
lakeblvd.net homepage
"""
from flask import render_template, request
from flask_login import current_user, login_required
import markdown
from . import bp

@bp.route('/', methods=["GET"])
def index():
    return render_template("home/index.html")

@bp.route('/about', methods=["GET", "POST"])
def about():
    with open('app/static/home/about.md') as file:
        md_content = file.read()
    md_html = markdown.markdown(md_content)
    return render_template("home/about-md.html", content=md_html)

@bp.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    # TODO: allow updating user profile
    # if request.method == "POST":
    #     form = 
    return render_template("home/profile.html", user=current_user)
