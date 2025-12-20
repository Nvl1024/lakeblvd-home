from flask import Blueprint

bp = Blueprint(
    'profile',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes