"""MUA API - Flask Application Initialization"""

from decouple import config
from flask import Flask
from flask_cors import CORS

from app.routes import main_bp


def create_app():
    app = Flask(__name__)

    # Habilita CORS para todas las rutas (puedes limitar dominios si lo deseas)
    CORS(app, origins=["https://mua-five.vercel.app/"])

    # Configura claves desde entorno
    app.config["MAILERLITE_API_KEY"] = config("MAILERLITE_API_KEY", default="")
    app.config["MAILERLITE_GROUP_ID"] = config("MAILERLITE_GROUP_ID", default="")  # noqa E501

    # Verifica que no falten las claves críticas
    if not app.config["MAILERLITE_API_KEY"]:
        app.logger.warning("MAILERLITE_API_KEY está vacío o no definido.")
    if not app.config["MAILERLITE_GROUP_ID"]:
        app.logger.warning("MAILERLITE_GROUP_ID está vacío o no definido.")

    # Registra las rutas
    app.register_blueprint(main_bp)

    return app
