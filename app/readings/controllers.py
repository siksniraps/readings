from flask import Blueprint

from app.readings.models import Reading

readings = Blueprint("readings", __name__, url_prefix="/reading")


@readings.route("/hello", methods=["GET"])
def hello():
    return "Hello, World!"
