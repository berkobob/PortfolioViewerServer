"""
09/08/18 - Antoine Lever - Run this script to start the Portfolio Viewer server
"""

import server.app as server
from data import data

server.run(debug=True)
