"""Test cases for the MUA API routes."""

import os
import sys

import pytest

from app import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # noqa: E501


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_ping(client):
    res = client.get("/ping")
    assert res.status_code == 200
    assert res.get_json() == {"message": "pong"}


def test_subscribe_validation(client):
    res = client.post("/subscribe", json={})
    assert res.status_code == 422
    assert "error" in res.get_json()
