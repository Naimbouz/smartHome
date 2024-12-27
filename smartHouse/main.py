import serial
from flask import Flask, render_template, request

app = Flask(__name__)

try:
    # Replace 'COM3' with your Arduino's COM port
    arduino = serial.Serial('COM3', 9600, timeout=1)
    print("Arduino connected successfully!")
except serial.SerialException as e:
    print(f"Error: {e}")
    arduino = None

@app.route('/')
def index():
    return render_template('dashboard.html')

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
