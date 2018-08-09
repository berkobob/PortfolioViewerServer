"""
09/08/18 - Portfolio Viewer Server
The web interface to the data model
"""

from flask import Flask
from server.api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def main():
    return("Hello Portfolio Viewer server world")