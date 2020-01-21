from datetime import datetime

import dateutil.parser
from dateutil.parser import ParserError
from flask import Blueprint, jsonify, request, abort, make_response

from app import db
from app.readings.models import Reading

readings = Blueprint("readings", __name__, url_prefix="/api/readings")


@readings.route("/", methods=["GET"])
def get_readings():
    return jsonify([reading.serialize() for reading in Reading.query.all()])


@readings.route("/<int:reading_id>", methods=["GET"])
def get_reading(reading_id):
    reading = Reading.query.get(reading_id)
    if reading is None:
        return make_response(jsonify({"message": "reading not found"}), 404)
    return jsonify(reading.serialize())


@readings.route("/", methods=["POST"])
def save_reading():
    args = validate(request)

    reading = Reading(args["value"], args["timestamp"])
    db.session.add(reading)
    db.session.commit()
    return jsonify(message="reading created")


@readings.route("/<int:reading_id>", methods=["PUT"])
def update_reading(reading_id):
    args = validate(request)
    rows_updated = db.session.query(Reading).filter_by(id=reading_id).update(
        {"value": args["value"], "timestamp": args["timestamp"]})
    if rows_updated == 1:
        db.session.commit()
        return jsonify(message="reading updated")
    else:
        return jsonify(message="reading not found"), 404


@readings.route("/<int:reading_id>", methods=["DELETE"])
def delete_reading(reading_id):
    if Reading.query.filter_by(id=reading_id).delete() == 1:
        db.session.commit()
        return jsonify(message="reading deleted")
    else:
        return jsonify(message="reading not found"), 404


def validate(reading_request):
    if "timestamp" in reading_request.form:
        try:
            timestamp = dateutil.parser.parse(reading_request.form["timestamp"])
        except ParserError:
            return abort(make_response(jsonify({"message": "bad timestamp format"}), 400))
    else:
        timestamp = datetime.now()

    if "value" not in reading_request.form:
        return abort(make_response(jsonify({"message": "reading value missing"}), 400))

    return {"value": reading_request.form["value"], "timestamp": timestamp}
