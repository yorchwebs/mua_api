"""MUA API - Flask Application Initialization"""

from decouple import config
from flask import Flask
from flask_cors import CORS

from app.routes import main_bp


def create_app():
    """Initialize the Flask application.

    Initializes the Flask application, sets up CORS, configures API keys, and registers routes.

    Returns:
        Flask: The initialized Flask application.
    """
    app = Flask(__name__)

    CORS(app, origins=["localhost:5000/contact"])

    app.config["MAILERLITE_API_KEY"] = config("MAILERLITE_API_KEY", default="")
    app.config["MAILERLITE_GROUP_ID"] = config(
        "MAILERLITE_GROUP_ID", default=""
    )

    if not app.config["MAILERLITE_API_KEY"]:
        app.logger.warning("MAILERLITE_API_KEY está vacío o no definido.")
    if not app.config["MAILERLITE_GROUP_ID"]:
        app.logger.warning("MAILERLITE_GROUP_ID está vacío o no definido.")

    app.register_blueprint(main_bp)

    return app
