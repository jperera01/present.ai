from flask import Flask, render_template


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
