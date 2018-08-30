"""
09/08/18 - Antoine Lever - Manage API requests
"""

from flask import Blueprint, jsonify, abort, request
from data import data
from server import controller

api = Blueprint('api', __name__)


@api.route('/')
def main():
    return jsonify({'msg': "The Portolio Viewer API home page"})


@api.route('/new', methods=['POST'])
def add_port():
    if not request.json or 'port' not in request.json:
        abort(400)

    port = request.json['port']

    e = data.new(port)
    if e:
        return jsonify({'result': e.__str__(), 'port': port}), 400
    return jsonify({'result': 'success', 'created': port}), 201


@api.route('/add', methods=['POST'])
def add_stock():
    if not request.json or 'port' not in request.json:
        abort(400)

    e = controller.add_stock(request.json)
    # e = data.add(request.json)

    if e:
        print(e)
        return jsonify({'result': e.__str__(),
                        'stock': request.json['ticker']}), 400
    return jsonify({'result': 'success', 'added': request.json['ticker']}), 201


@api.route('/ports', methods=['GET'])
def get_ports():
    ports = data.ports()
    try:
        return jsonify({"result": 'success', 'ports': ports}), 200
    except Exception as e:
        return jsonify({"result": ports.__str__()}), 500


@api.route('/<port>', methods=['GET'])
def get_stocks(port):
    stocks = data.stocks(port)
    try:
        return jsonify({'result': 'success', 'port': port,
                        'stocks': stocks}), 200
    except Exception as e:
        return jsonify({'result': stocks.__str__()})


@api.route('/del', methods=['POST'])
def delete():
    if not request.json or 'port' not in request.json:
        abort(400)

    port = request.json['port']
    stocks = request.json['stock']

    if len(stocks) == 0:
        e = data.del_port(port)
        if e:
            return jsonify({'result': e.__str__(), 'port': port}), 400
        return jsonify({'result': 'success', 'deleted': port}), 201

    for stock in stocks:
        print("OK, lets delete", stock)
        e = data.del_stock(port, stock)
        if e:
            print(e.text)
    return jsonify({"result": 'success', 'stocks': stocks})
