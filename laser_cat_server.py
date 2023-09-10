#!/usr/bin/env python

import pantilthat
from sys import exit

try:
    from flask import Flask, render_template
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('gui.html')

@app.route('/api/<int(signed=True):x>/<int(signed=True):y>', methods=['GET'])
def api(x, y):
    tiltAngle = y
    print(x, y, 'x, y')
    panAngle = x

    if x > 0 or x < 0:
        pantilthat.pan(panAngle)

    if y < 0 or y > 0:
        pantilthat.tilt(tiltAngle)

    return "{'error':'invalid direction'}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)
