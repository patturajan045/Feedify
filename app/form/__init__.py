from flask import Blueprint

formBp = Blueprint("formBp", __name__)

from . import routes
