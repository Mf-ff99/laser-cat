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

@app.route('/api/int:<x>/int:<y>')
def api(x, y):
    panAngle = y * 100
    print(y * 100, x * 100)
    tiltAngle = x * 100

    if x > 0 or x < 0:
        pantilthat.pan(panAngle)
        return "{{'pan':{}}}".format(panAngle)

    elif y < 0 or y > 0:
        pantilthat.tilt(tiltAngle)
        return "{{'tilt':{}}}".format(tiltAngle)

    return "{'error':'invalid direction'}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)
