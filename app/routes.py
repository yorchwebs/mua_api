"""MUA API - Main Routes"""

import requests
from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError

from app.schemas import SubscriptionSchema

main_bp = Blueprint("main", __name__)


@main_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})


@main_bp.route("/subscribe", methods=["POST"])
def subscribe():
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
