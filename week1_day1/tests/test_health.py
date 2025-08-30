"""Unit tests for the health check endpoint."""

from fastapi.testclient import TestClient
from week1_day1.app.main import app

client = TestClient(app)


def test_health_check():
    """Test that the /health endpoint returns status code 200 and expected JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
