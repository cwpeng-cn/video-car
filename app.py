from flask import Flask, render_template, Response
import cv2
import RPi.GPIO as GPIO

app = Flask(__name__)


class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        success, image = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/forward', methods=['GET'])
def forward():
    print("forward")
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.HIGH)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.HIGH)
    return "200"


@app.route('/left', methods=['GET'])
def left():
    print("left")
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.HIGH)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.LOW)
    return "200"


@app.route('/right', methods=['GET'])
def right():
    print("right")
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.HIGH)
    return "200"


@app.route('/stop', methods=['GET'])
def stop():
    print("stop")
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.LOW)
    return "200"


def _init_():
    GPIO.setmode(GPIO.BCM)
    for i in range(22):
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.LOW)


if __name__ == '__main__':
    _init_()
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='192.168.1.19', port=5000)
