#!/usr/bin/python3
"""
Tihs file uses the created Blueprint to define routes
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


classTexts = {
  "amenities": "Amenity",
  "cities": "City",
  "places": "Place",
  "reviews": "Review",
  "states": "State",
  "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    """
    returns a status ok
    """
    json_data = {
        "status": "OK"
    }
    return jsonify(json_data)


@app_views.route('/stats', strict_slashes=False)
def objects_count():
    """
    This retrieves the number of each object by type
    """
    stats = {}
    for key, value in classTexts.items():
        stats[key] = storage.count(value)

    return jsonify(stats)


if __name__ == "__main__":
    pass
