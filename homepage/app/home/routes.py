"""
lakeblvd.net homepage
"""
from flask import render_template, request
from flask_login import current_user, login_required
import markdown
import bleach
from . import bp

@bp.route('/', methods=["GET"])
def index():
    return render_template("home/index.html")

@bp.route('/about', methods=["GET", "POST"])
def about():
    with open('app/static/home/about.md', 'r', encoding="utf-8") as file:
        md_content = file.read()
    # TODO: write a utility function to handle bleaching, rendering, etc.
    # md_content >> safe_html
    md_html = markdown.markdown(
        md_content,
        extensions=["fenced_code", "tables", "extra", "smarty"])
    # clean up the html
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) \
        + ["p", "pre", "code", "h1", "h2", "h3", "table", "thead", \
           "tbody", "tr", "th", "td", "ul", "ol", "li", "blockquote"]
    allowed_attrs = {"a": ["href", "title", "rel", "target"], "img": ["src", "alt", "title"]}
    safe_html = bleach.clean(md_html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    return render_template("home/about-md.html", content=safe_html)

