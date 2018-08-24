"""
09/08/18 - Portfolio Viewer Server
The web interface to the data model
"""

from flask import Flask, request, render_template, redirect
from server.api import api
from data import data
from server import controller

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/', methods=['GET', 'POST'])
def main():
    """ home page. show list of portfolios and their values """
    if request.method == 'POST':
        data.new(request.form['name'])

    ports = data.ports()

    return render_template('home.html', ports=data.ports())

@app.route('/<port>/', methods=['GET', 'POST'])
def port(port):
    if request.method == 'POST':
        return render_template('home.html', ports=data.ports())

    ports = data.ports()
    stocks = data.stocks(port)
    return render_template('port.html', ports=ports, tickers=stocks, page=port)

@app.route('/load/', methods=['POST'])
def load():
    if request.method == 'POST':
        f=request.files['file']
        f.save(f.filename)
        controller.load_port(request.form['name'], f.filename)
    return redirect('/')

@app.route('/del/<port>', methods=['GET'])
def del_port(port):
    data.del_port(port)
    return redirect('/')

@app.route('/<port>/<col>/', methods=['GET'])
def sort_port(port, col):
    controller.sort_port(port, col)
    return redirect('/'+port)