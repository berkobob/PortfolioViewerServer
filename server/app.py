"""
09/08/18 - Portfolio Viewer Server
The web interface to the data model
"""
import os
from flask import Flask, request, render_template, redirect, flash
from server.api import api
from data import data
from server import controller

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.secret_key = os.urandom(24)

reverse = False

@app.route('/', methods=['GET', 'POST'])
def main():
    """ home page. show list of portfolios and their values """
    if request.method == 'POST':
        e = data.new(request.form['name'])
        if e:
            flash(str(e))

    ports = data.ports()
    if isinstance(ports, list):
        return render_template('home.html', ports=data.ports())
    return str(ports)

@app.route('/<port>/', methods=['GET', 'POST'])
def view_port(port, sort=1):
    if request.method == 'POST':
        return render_template('home.html'), 500

    stocks = data.stocks(port)
    if isinstance(stocks, list):
        stocks.sort(key=lambda stock: stock[sort], reverse=reverse)
        return render_template('port.html', tickers=stocks, page=port)
    #return render_template('500.html', message=str(stocks)), 500
    message = "Failed to load portfolio "+port+" because: "+str(stocks)
    flash(message)
    return redirect('/')

@app.route('/load/', methods=['POST'])
def load():
    if request.method == 'POST':
        f=request.files['file']
        f.save(f.filename)
        e = controller.load_port(request.form['name'], f.filename)
        if e:
            flash("Cannot load file because: "+str(e))
    return redirect('/')

@app.route('/del/<port>', methods=['GET'])
def del_port(port):
    e = data.del_port(port)
    if e:
        flash(str(e))
    return redirect('/')

@app.route('/<port>/<col>/', methods=['GET'])
def sort_port(port, col):
    global reverse 
    reverse = not reverse
    return view_port(port, int(col))