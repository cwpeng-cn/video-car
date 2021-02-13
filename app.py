from flask import Flask, render_template, Response, request, redirect
import cv2
import RPi.GPIO  as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)


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
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.HIGH)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.HIGH)
    return redirect("/")


@app.route('/left', methods=['GET'])
def left():
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.HIGH)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.LOW)
    return redirect("/")


@app.route('/right', methods=['GET'])
def right():
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.HIGH)
    return redirect("/")


@app.route('/stop', methods=['GET'])
def stop():
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)
    GPIO.setup(9, GPIO.OUT)
    GPIO.output(9, GPIO.LOW)
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
