# Import flask and template operators
from flask import Flask, jsonify

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify(message="not found"), 404


# Import a module / component using its blueprint handler variable (mod_auth)
from app.readings.controllers import readings as readings

# Register blueprint(s)
app.register_blueprint(readings)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
