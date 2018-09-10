"""
09/08/18 - Portfolio Viewer Server
The web interface to the data model
"""
import os
from flask import Flask, request, render_template, redirect, flash, url_for, \
    session
from server.api import api
from server.login import requires_login
from server import controller

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
# app.secret_key = os.urandom(24)
app.secret_key = "123"


@app.route('/', methods=['GET', 'POST'])
@requires_login
def main():
    """ home page. show list of portfolios and their values
        and POST is to create a new port """
    if request.method == 'POST':
        controller.new(session['user'], request.form['name'])

    return render_template('home.html',
                           ports=controller.ports(session['user']))


@app.route('/<port>/', methods=['GET', 'POST'])
@requires_login
def view_port(port, sort='name'):
    """ port page. Shows all stocks in port and allow add stock to port """
    if request.method == 'POST':
        stock = request.form.to_dict()
        stock['user'] = session['user']
        stock['port'] = port
        controller.add_stock(stock)
        # Here not in controller.add_stock to just do it once per load
        controller.update_stocks(session['user'], port)

    stocks = controller.get_port(session['user'], port)
    stocks.sort(key=lambda stock: stock[sort], reverse=session['dir'])
    return render_template('port.html', tickers=stocks, page=port)


@app.route('/load/', methods=['POST'])
@requires_login
def load():
    f = request.files['file']
    f.save(f.filename)
    controller.load_port(session['user'], request.form['name'], f.filename)
    controller.update_port(session['user'], request.form['name'])
    return redirect('/')


@app.route('/del/<port>', methods=['GET'])
@requires_login
def del_port(port):
    controller.del_port(session['user'], port)
    return redirect('/')


@app.route('/<port>/<col>/', methods=['GET'])
@requires_login
def sort_port(port, col):
    session['dir'] = not session['dir']
    return view_port(port, col)


@app.route('/del/<port>/<stock>/', methods=['GET'])
@requires_login
def del_stock(port, stock):
    controller.del_stock(port, stock)
    controller.update_port(session['user'], port)
    return view_port(port, sort='name')


@app.route('/update/<port>', methods=['GET'])
@requires_login
def update(port):
    controller.update_stocks(session['user'], port)
    return view_port(port)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if controller.is_user(request.form['username'],
                              request.form['password']):
            session['user'] = request.form['username']
            session['dir'] = False
            return redirect('/')

    return render_template("login.html")


@app.route('/logout/', methods=['GET'])
def logout():
    session.pop('user')
    return("Bye")
