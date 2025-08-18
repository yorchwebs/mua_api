"""MUA API - Main Routes"""

import smtplib
from email.mime.text import MIMEText

import requests
from decouple import config
from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError

from app.schemas import SubscriptionSchema

SMTP_HOST = config("SMTP_HOST")
SMTP_PORT = config("SMTP_PORT", cast=int)
SMTP_USER = config("SMTP_USER")
SMTP_PASSWORD = config("SMTP_PASSWORD")
SMTP_FROM = config("SMTP_FROM")
SMTP_TO = config("SMTP_TO", default=SMTP_USER)

main_bp = Blueprint("main", __name__)


@main_bp.route("/subscribe", methods=["POST"])
def subscribe():
    """Subscribe a user to the mailing list

    Args:
        email (str): The email address of the user to subscribe.
        groups (list): The groups to which the user should be added.

    Returns:
        dict: A dictionary containing the status of the subscription.


    Example:
        {
            "email": "example@example.com",
            "groups": [123456789]
        }
    """
    try:
        json_data = request.get_json()
        data = SubscriptionSchema(**json_data)
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 422

    api_key = current_app.config.get("MAILERLITE_API_KEY")
    group_id = current_app.config.get("MAILERLITE_GROUP_ID")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "email": data.email,
    }

    if group_id:
        payload["groups"] = [int(group_id)]

    response = requests.post(
        "https://connect.mailerlite.com/api/subscribers",
        json=payload,
        headers=headers,
    )

    if response.status_code in [200, 201]:
        return jsonify({"message": "Suscripción exitosa"}), 200
    else:
        return jsonify(
            {"error": "Error al suscribirse", "details": response.json()}
        ), response.status_code


@main_bp.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submissions

    Args:
        name (str): The name of the person submitting the form.
        email (str): The email address of the person submitting the form.
        phone (str): The phone number of the person submitting the form.
        message (str): The message from the contact form.

    Returns:
        dict: A dictionary containing the status of the email sending.

    Example:
        {
            "name": "Usuario Prueba",
            "email": "correo@correo.com",
            "phone": "123456789",
            "message": "This is a test message."
        }
    """
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    if not all([name, email, phone, message]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        body = f"Nuevo mensaje de: {name}\n\n Mis medios de contacto: {email}, {phone}\n\n{message}"  # noqa: E501

        msg = MIMEText(body, "plain")
        msg["Subject"] = "Nuevo mensaje de contacto"
        msg["From"] = SMTP_FROM
        msg["To"] = SMTP_TO

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, SMTP_TO, msg.as_string())

        return jsonify({"success": True, "message": "Email sent"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
