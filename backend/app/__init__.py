from flask import Flask, render_template
from flask_sock import Sock
import threading
import base64
import io
import json
from flask_restx import Api
from app.exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import speech_recognition as sr
from pydub import AudioSegment
from app.models import User
from app.main import main_bp
from app.dashboard import dashboard_bp
from app.present import present_bp
from app.api.auth import auth_ns
from app.api.api import api_ns
from app.config import DevConfig

# sam = True


r = sr.Recognizer()


def convert_ogg_to_wav(ogg_data):
    audio = AudioSegment.from_file(io.BytesIO(ogg_data), format="ogg")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io


def process_audio(data, ws):
    try:
        wav_audio = convert_ogg_to_wav(data)

        with sr.AudioFile(wav_audio) as source:
            audio = r.record(source)

            try:
                text = r.recognize_google(audio)
                ws.send(text)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


def create_app():
    app = Flask(__name__)  # added static_folder to allow images
    sock = Sock(app)

    # r.recognize_google()

    app.config.from_object(DevConfig)

    db.init_app(app)

    migrate = Migrate(app, db)

    JWTManager(app)

    @sock.route('/handle-stream')
    def handle_stream(ws):
        global sam
        while True:
            message = ws.receive()
            if message is None:
                break

            message = json.loads(message)

            if message['type'] == "audio":
                binary_data = base64.b64decode(message['data'])
                threading.Thread(target=process_audio,
                                 args=(binary_data, ws)).start()

            elif message['type'] == "video":
                ...

            # handle new receive
            # if sam:
            # sam = False
            # _, encoded = received.split(",", 1)

            # image_data = base64.b64decode(encoded)
            # with open(f"image.jpg", "wb") as file:
            # file.write(image_data)

    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(present_bp)

    api = Api(app, doc="/docs")

    api.add_namespace(auth_ns)
    api.add_namespace(api_ns)

    @app.shell_context_processor
    def make_shell_context():
        db.create_all()
        return {
            "db": db,
            "user": User
        }

    return app
