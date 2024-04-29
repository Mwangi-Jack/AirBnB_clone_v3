#!/usr/bin/python3

"""
This file is the entry point of the api it registers
a Blueprint which will be used to define routes
"""

from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """
    Closes the storage when the application context ends
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """"custom not found (404) response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
