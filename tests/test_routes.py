"""Test cases for the MUA API routes."""

import os
import sys
from unittest.mock import Mock, patch

import pytest

from app import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # noqa: E501


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["MAILERLITE_API_KEY"] = "fake-key"
    app.config["MAILERLITE_GROUP_ID"] = "123456"
    return app.test_client()


def test_ping(client):
    res = client.get("/ping")
    assert res.status_code == 200
    assert res.get_json() == {"message": "pong"}


def test_subscribe_validation(client):
    res = client.post("/subscribe", json={})
    assert res.status_code == 422
    assert "error" in res.get_json()


@patch("app.routes.requests.post")
def test_subscribe_success(mock_post, client):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"message": "OK"}

    mock_post.return_value = mock_response

    response = client.post("/subscribe", json={"email": "test@mail.com"})

    assert response.status_code == 200
    assert response.get_json()["message"] == "Suscripción exitosa"


@patch("app.routes.requests.post")
def test_subscribe_failure(mock_post, client):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"message": "Subscriber already exists"}

    mock_post.return_value = mock_response

    response = client.post("/subscribe", json={"email": "test@mail.com"})

    assert response.status_code == 400
    body = response.get_json()
    assert "error" in body
    assert "details" in body
    assert body["details"]["message"] == "Subscriber already exists"


def test_subscribe_validation_error(client):
    response = client.post("/subscribe", json={"email": "not-an-email"})

    assert response.status_code == 422
    body = response.get_json()
    assert "error" in body
    assert "details" in body
