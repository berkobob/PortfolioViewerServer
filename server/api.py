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

    port = request.json['port']

    e = data.new(port)
    if e:
        print(e)
        return jsonify({'result': e.__str__(), 'port': port}), 400
    return jsonify({'result': 'success', 'create': port}), 201

@api.route('/add', methods=['POST'])
def add_stock():
    if not request.json or not 'port' in request.json:
        abort(400)

    e = data.add(request.json)
    if e:
        print (e) 
        return jsonify({'result': e.__str__(), 'stock': request.json['name']}), 400
    return jsonify({'result': 'success', 'stock': request.json['name']}), 201