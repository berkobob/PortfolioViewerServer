"""
09/08/18 - Antoine Lever - Manage API requests
"""

from flask import Blueprint, jsonify, abort, request
from data import data

api = Blueprint('api', __name__)

@api.route('/')
def main():
    return jsonify({'msg': "The Portolio Viewer API home page"})

@api.route('/new', methods=['POST'])
def add_port():
    if not request.json or not 'port' in request.json:
        abort(400)

    data.new(request.json['port'])
    return jsonify({'port': request.json['port']}), 201
