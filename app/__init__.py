"""MUA API - Flask Application Initialization"""

from decouple import config
from flask import Flask
from flask_cors import CORS

from app.routes import main_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    CORS(app)

    # Ejemplo de carga de variable (verifica que no falle)
    app.config["MAILERLITE_API_KEY"] = config("MAILERLITE_API_KEY", default="")
    app.config["MAILERLITE_GROUP_ID"] = config("MAILERLITE_GROUP_ID", default="")  # noqa: E501

    return app
