import serial
from flask import Flask, render_template, request, jsonify
import threading

app = Flask(__name__)

try:
    arduino = serial.Serial('COM3', 9600, timeout=1)  # Update COM port as needed
    print("Arduino connected successfully!")
except serial.SerialException as e:
    print(f"Error: {e}")
    arduino = None

distance_data = "Waiting for data..."  # Global variable for distance

# Background thread to read distance data
def read_distance():
    global distance_data
    while True:
        if arduino and arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            if line.startswith("D:"):
                distance_data = line[2:] + " cm"  # Extract distance value

# Start background thread
threading.Thread(target=read_distance, daemon=True).start()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/distance', methods=['GET'])
def get_distance():
    global distance_data
    return jsonify({"distance": distance_data})

@app.route('/led', methods=['POST'])
def led():
    if arduino:
        state = request.form['state']
        if state == 'on':
            arduino.write(b'1')  # Send '1' to turn on LED
        elif state == 'off':
            arduino.write(b'0')  # Send '0' to turn off LED
    return "OK"

if __name__ == '__main__':
    app.run(debug=False)
