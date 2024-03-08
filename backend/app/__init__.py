from flask import Flask, render_template
from flask_sock import Sock
import base64
import json
from app.main import main_bp
from app.present import present_bp

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

            message = json.loads(received)

            if message['type'] == "audio":
                ...
            elif message['type'] == "video":
                ...

            # handle new receive
            # if sam:
            # sam = False
            # _, encoded = received.split(",", 1)

            # image_data = base64.b64decode(encoded)
            # with open(f"image.jpg", "wb") as file:
            # file.write(image_data)

    app.config.from_object(config)

    app.register_blueprint(main_bp)
    app.register_blueprint(present_bp)

    return app
