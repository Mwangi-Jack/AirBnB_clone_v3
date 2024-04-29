#!/usr/bin/python3

"""
This file handles all the default  RESTFul API
actions (CRUD)
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_of_state(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    all_cities = storage.all("City")
    cities = []

    for value in all_cities.values():
        if value.state_id == state_id:
            cities.append(value.to_dict())

    if len(cities) == 0:
        abort(404)

    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """

    city = storage.get(City, city_id)

    if city is not None:
        return city.to_dict()

    abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object given the city id
    """

    city = storage.get(City, city_id)

    if city is not None:
        storage.delete(city)
        storage.save()

        return make_response({}, 200)

    abort(404)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City object
    """

    state = storage.get("State", state_id)

    if state is not None:
        request_body = request.get_json()
        if not request.is_json:
            abort(404, description='Not a JSON')

        if 'name' not in request_body:
            abort(404, description="Missing name")

        request_body['state_id'] = state_id
        city = City(**request_body)
        city.save()

        return make_response(city.to_dict(), 201)

    abort(404)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a city object with the given city_id
    """

    city = storage.get("City", city_id)

    if city is not None:
        request_body = request.get_json()

        if not request.is_json:
            abort(404, 'Not a JSON')

        for k, v in request_body.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)

        city.save()
        return make_response(city.to_dict(), 200)

    abort(404)
