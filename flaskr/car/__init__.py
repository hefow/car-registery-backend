from flask import Blueprint

bp = Blueprint("car",__name__,url_prefix="/api/car")

from . import routes