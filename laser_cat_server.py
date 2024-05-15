#!/usr/bin/env python
import time
import pantilthat
from sys import exit
import threading

# Constants for smoothing
alpha = 0.01  # tune smoothness with this
deadzone = 5

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
        # Apply smooth movement towards the target angles
        new_pan_angle = smooth_move(target_pan_angle, current_pan_angle)
        new_tilt_angle = smooth_move(target_tilt_angle, current_tilt_angle)

        # Update the servo positions if there's any change
        if new_pan_angle != current_pan_angle:
            pantilthat.pan(int(new_pan_angle))
            current_pan_angle = new_pan_angle

        if new_tilt_angle != current_tilt_angle:
            pantilthat.tilt(int(new_tilt_angle))
            current_tilt_angle = new_tilt_angle

        # Sleep briefly to avoid overloading the CPU and servos
        time.sleep(0.05)

def smooth_move(target, current):
    if abs(target - current) > deadzone:
        # Apply exponential smoothing
        return current + alpha * (target - current)
    else:
        return current
    
def set_new_target(pan, tilt):
    global target_pan_angle, target_tilt_angle
    target_pan_angle = pan
    target_tilt_angle = tilt

servo_thread = threading.Thread(target=update_servos)
servo_thread.daemon = True  # Allows the thread to exit when the main program does
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

    # Apply constraints to pan and tilt angles
    # Apply constraints to pan and tilt angles
    panAngle = 90 if x > 90 else (-90 if x < -90 else x)
    tiltAngle = 90 if y > 90 else (-90 if y < -90 else y)

    # Smoothly update the pan angle
    set_new_target(tiltAngle, invert_integer(panAngle))

    return "{'error':'invalid direction'}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)
