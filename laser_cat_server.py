  GNU nano 5.4                                                                                laser_cat_server.py
#!/usr/bin/env python
import time
import pantilthat
from sys import exit
import threading

alpha = 0.10  # tune smoothness with this
deadzone = 2
sensitivity = 0.1  # joystick sensitivity

current_pan_angle = 0
current_tilt_angle = 0
target_pan_angle = 0
target_tilt_angle = 0

try:
    from flask import Flask, render_template
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

app = Flask(__name__)

def update_servos():
    global current_pan_angle, current_tilt_angle
    while True:

        new_pan_angle = smooth_move(target_pan_angle, current_pan_angle)
        new_tilt_angle = smooth_move(target_tilt_angle, current_tilt_angle)

        if new_pan_angle != current_pan_angle:
            pantilthat.pan(int(new_pan_angle))
            current_pan_angle = new_pan_angle

        if new_tilt_angle != current_tilt_angle:
            pantilthat.tilt(int(new_tilt_angle))
            current_tilt_angle = new_tilt_angle
       # adjust refresh rate
        time.sleep(0.01)

def smooth_move(target, current):
    if abs(target - current) > deadzone:
        # exponential smoothing
        return current + alpha * (target - current)
    else:
        return current

def set_new_target(pan_delta, tilt_delta):
    global target_pan_angle, target_tilt_angle
    target_pan_angle += pan_delta
    target_tilt_angle += tilt_delta

    # constraints to pan and tilt angles
    target_pan_angle = min(90, max(-90, target_pan_angle))
    target_tilt_angle = min(90, max(-90, target_tilt_angle))

servo_thread = threading.Thread(target=update_servos)
servo_thread.daemon = True
servo_thread.start()

@app.route('/')
def home():
    return render_template('gui.html')

@app.route('/api/<int(signed=True):x>/<int(signed=True):y>', methods=['GET'])
def api(x, y):
    global current_pan_angle, current_tilt_angle

    print(x, y, 'x, y')

    def invert_integer(n):
        return -n

    # deltas based on joystick inputs
    pan_delta = x * sensitivity
    tilt_delta = y * sensitivity

    # update pan and tilt angle setpoints
    set_new_target(invert_integer(pan_delta), invert_integer(tilt_delta))

    return "{'error':'invalid direction'}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)
