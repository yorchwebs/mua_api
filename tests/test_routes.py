"""Test cases for the MUA API routes."""

import email
import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

from app import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # noqa: E501


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask application."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["MAILERLITE_API_KEY"] = "fake-key"
    app.config["MAILERLITE_GROUP_ID"] = "123456"
    return app.test_client()


# Test cases for the /subscribe route


def test_subscribe_validation(client):
    """If any required fields are missing, it should return a 422 error.

    Args:
        client (FlaskClient): Test client used to send requests to the API.

    Returns:
        None: Verifies that validation is handled correctly and a 422 error is returned.

    Example:
        {
            "email": "correo@correo.com",
            "error": "Invalid input",
            "details": {"email": ["Invalid email address"]}
        }
    """

    res = client.post("/subscribe", json={})
    assert res.status_code == 422
    assert "error" in res.get_json()


@patch("app.routes.requests.post")
def test_subscribe_success(mock_post, client):
    """Success case: successful subscription

    Args:
        mock_post (MagicMock): Mock of the requests.post function to simulate
            a successful response from the MailerLite API.
        client (FlaskClient): Test client used to send requests to the API.

    Returns:
        None: Verifies that the subscription is handled correctly and a success
            message is returned.

    Example:
        {
            "email": "correo@correo.com",
            "message": "Successful subscription"
        }
    """

    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"message": "OK"}

    mock_post.return_value = mock_response

    response = client.post("/subscribe", json={"email": "test@mail.com"})

    assert response.status_code == 200
    assert response.get_json()["message"] == "Suscripción exitosa"


@patch("app.routes.requests.post")
def test_subscribe_failure(mock_post, client):
    """Error case: subscription failed

    Args:
        mock_post (MagicMock): Mock of the requests.post function to simulate
            an error response from the MailerLite API.
        client (FlaskClient): Test client used to send requests to the API.

    Returns:
        None: Verifies that the error is handled correctly and an error message
            is returned.

    Example:
        {
            "email": "correo@correo.com",
            "error": "Subscription failed",
            "details": {"message": "Subscriber already exists"}
        }
    """

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
    """If the email is invalid, it should return a 422 error.

    Args:
        client (FlaskClient): Test client used to send requests to the API.

    Returns:
        None: Verifies that email validation is handled correctly and a 422 error
            is returned.

    Example:
        {
            "email": "not-an-email",
            "error": "Invalid input",
            "details": {"email": ["Invalid email address"]}
        }
    """

    response = client.post("/subscribe", json={"email": "not-an-email"})

    assert response.status_code == 422
    body = response.get_json()
    assert "error" in body
    assert "details" in body


# Test cases for the /contact route


def test_contact_missing_fields(client):
    """If any required fields are missing, it should return a 400 error."""
    res = client.post("/contact", json={})
    assert res.status_code == 400
    body = res.get_json()
    assert "error" in body
    assert body["error"] == "Missing fields"


@patch("app.routes.smtplib.SMTP")
def test_contact_success(mock_smtp, client):
    """Success case: email sent successfully

    Args:
        mock_smtp (MagicMock): Mock of the SMTP client to simulate
            email sending.
        client (FlaskClient): Test client used to send requests to the API.

    Returns:
        None: Verifies that the email is sent correctly and a success
            message is returned.

    Example:
        {
            "name": "Yorch",
            "email": "email@email.com",
            "phone": "123456789",
            "message": "Hello, this is a test"
        }
    """

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    payload = {
        "name": "Yorch",
        "email": "user@test.com",
        "phone": "123456789",
        "message": "Hola, este es un test",
    }

    res = client.post("/contact", json=payload)

    assert res.status_code == 200
    body = res.get_json()
    assert body["success"] is True
    assert body["message"] == "Email sent"

    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.sendmail.assert_called_once()

    args, kwargs = mock_server.sendmail.call_args
    from_addr, to_addrs, msg_raw = args

    msg_obj = email.message_from_string(msg_raw)

    assert msg_obj["Subject"] == "Nuevo mensaje de contacto"
    assert msg_obj["From"] == "contacto@yorchwebs.com"
    assert msg_obj["To"] != ""

    body_content = msg_obj.get_payload()
    assert "Yorch" in body_content
    assert "user@test.com" in body_content
    assert "123456789" in body_content
    assert "Hola, este es un test" in body_content


@patch("app.routes.smtplib.SMTP", side_effect=Exception("SMTP failure"))
def test_contact_failure(mock_smtp, client):
    """Error case: email sending failed

    Args:
        mock_smtp (MagicMock): Mock of the SMTP client to simulate a failure
            during email sending.
        client (FlaskClient): Test client used to send requests to the API.

    Returns:
        None: Verifies that the exception is handled correctly and an error
            message is returned.

    Example:
        {
            "name": "Yorch",
            "email": "correo@correo.com",
            "phone": "123456789",
            "message": "Test failure"
        }
    """
    payload = {
        "name": "Yorch",
        "email": "user@test.com",
        "phone": "123456789",
        "message": "Falla de prueba",
    }

    res = client.post("/contact", json=payload)

    assert res.status_code == 500
    body = res.get_json()
    assert "error" in body
    assert "SMTP failure" in body["error"]
