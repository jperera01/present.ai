from flask import Flask, render_template
from flask_sock import Sock
import base64

# sam = True


def create_app(config):
    app = Flask(__name__)
    sock = Sock(app)

    @sock.route('/handle-stream')
    def handle_stream(ws):
        global sam
        while True:
            received = ws.receive()
            if received is None:
                break

            # handle new receive
            # if sam:
                # sam = False
                # _, encoded = received.split(",", 1)

                # image_data = base64.b64decode(encoded)
                # with open(f"image.jpg", "wb") as file:
                # file.write(image_data)

    app.config.from_object(config)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
