#!/usr/bin/python3
"""
This file defines the routes to perform operations
on the States class
"""

from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """
    Retrieves  the list of all State objects
    """
    states_obj = []

    for value in storage.all("State").values():
        states_obj.append(value.to_dict())

    return jsonify(states_obj)


@app_views.route("/states/<state_id>", strict_slashes=False)
def one_state(state_id):
    """
    this method returns a specific state depending on the
    id passed in
    """
    all_states = storage.all("State")

    for value in all_states.values():
        if value.id == state_id:
            return jsonify(value.to_dict())

    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a state given the id
    """
    state = storage.get(State, state_id)

    if state is not None:
        storage.delete(state)
        storage.save()
        return make_response({}, 200)

    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    creates a state
    """
    if not request.is_json:
        abort(400, description='Not a JSON')

    request_body = request.get_json()

    if 'name' not in request_body:
        abort(400, description='Missing name')

    new_state = State(**request_body)
    storage.new(new_state)
    storage.save()
    return make_response(new_state.to_dict(), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates a state given the id
    """

    if not request.is_json:
        abort(400, description="Not a JSON")

    request_data = request.get_json()
    state = storage.get(State, state_id)

    if state is not None:
        for k, v in request_data.items():
            if k not in ['id', 'updated_at', 'created_at']:
                setattr(state, k, v)
        state.save()
        return state.to_dict()

    abort(404)
