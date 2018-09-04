"""
09/08/18 - Portfolio Viewer Server
The web interface to the data model
"""
import os
import copy
from flask import Flask, request, render_template, redirect, flash, url_for, \
    session
from server.api import api
from server.login import requires_login
from data import data
from server import controller

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.secret_key = os.urandom(24)

reverse = False


@app.route('/', methods=['GET', 'POST'])
@requires_login
def main():
    """ home page. show list of portfolios and their values
        and POST is to create a new port """
    if request.method == 'POST':
        data.new(request.form['name'])

    return render_template('home.html', ports=controller.ports())


@app.route('/<port>/', methods=['GET', 'POST'])
@requires_login
def view_port(port, sort='name'):
    if request.method == 'POST':
        stock = request.form.to_dict()
        stock['port'] = port
        controller.add_stock(stock)
        controller.update_stocks(port)  # Here not in controller.add_stock
                                        # to just do it once per load
    stocks = controller.get_port(port)
    stocks.sort(key=lambda stock: stock[sort], reverse=reverse)
    return render_template('port.html', tickers=stocks, page=port)


@app.route('/load/', methods=['POST'])
@requires_login
def load():
    f = request.files['file']
    f.save(f.filename)
    controller.load_port(request.form['name'], f.filename)
    return redirect('/')


@app.route('/del/<port>', methods=['GET'])
@requires_login
def del_port(port):
    data.del_port(port)
    return redirect('/')


@app.route('/<port>/<col>/', methods=['GET'])
@requires_login
def sort_port(port, col):
    global reverse
    reverse = not reverse
    return view_port(port, col)


@app.route('/del/<port>/<stock>/', methods=['GET'])
@requires_login
def del_stock(port, stock):
    data.del_stock(port, stock)
    controller.update_port(port)
    return view_port(port, sort='name')


@app.route('/update/<port>', methods=['GET'])
@requires_login
def update(port):
    controller.update_stocks(port)
    return view_port(port)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if controller.is_user(request.form['username'],
                              request.form['password']):
            session['user'] = request.form['username']
            return redirect('/')

    return render_template("login.html")
