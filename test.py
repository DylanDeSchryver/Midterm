from flask import Flask, request, jsonify
from adafruit_motorkit import MotorKit
import time
# Initialize the MotorKit
kit = MotorKit(0x40)

app = Flask(__name__)


@app.route('/move', methods=['POST'])
def process():
    command = request.json['direction']
    if command == 'forward':
        move_forward()
    elif command == 'backward':
        move_backward()
    elif command == 'left':
        turn_left()
    elif command == 'right':
        turn_right()
    elif command == 'stop':
        stop_robot()



# Define movement functions
def move_forward():
    kit.motor1.throttle = 0.77
    kit.motor2.throttle = 0.73
    robot_state = "moving forward"
def move_backward():
    kit.motor1.throttle = -0.80
    kit.motor2.throttle = -0.76
    robot_state = "moving backward"

def turn_left():
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = -0.75
    robot_state = "turning left"

def turn_right():
    kit.motor1.throttle = -0.76
    kit.motor2.throttle = 0.75
    robot_state = "turning right"

def stop_robot():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0
    robot_state = "stopped"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #must be using 0.0.0.0 because this ensures that the server can be accessed from other computers.
#the default 127.0.0.1 doesnt allow other computers except the one running the server to process requests.



