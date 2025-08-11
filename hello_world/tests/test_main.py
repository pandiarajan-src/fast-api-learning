"""
Unit tests for the FastAPI application in hello_world.main.
"""

import pytest
from fastapi.testclient import TestClient
from hello_world.main import app, _USERS, _STATE

client = TestClient(app)


def setup_function():
    """Reset in-memory store before each test."""
    _USERS.clear()
    _STATE["next_id"] = 1


def test_read_root():
    """Test the root endpoint returns the welcome message."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello FastAPI!!!"}


def test_echo_post():
    """Test the echo endpoint with a non-empty string."""
    payload = {"text": "hello"}
    resp = client.post("/echo", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"echo": "HELLO", "echo_length": 5}


def test_echo_post_empty():
    """Test the echo endpoint with an empty string."""
    payload = {"text": ""}
    resp = client.post("/echo", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"echo": "", "echo_length": 0}


@pytest.mark.parametrize("name", ["Alice", "Bob", "Pandi"])
def test_greet(name):
    """Test the greet endpoint with valid names."""
    resp = client.get(f"/greet/{name}")
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Hello {name}!!!"}


def test_greet_invalid_name():
    """Test the greet endpoint with a missing name (should 404)."""
    resp = client.get("/greet/")
    assert resp.status_code == 404  # path param required


def test_greet_name_too_long():
    """Test the greet endpoint with a name that's too long (should 422)."""
    name = "a" * 51
    resp = client.get(f"/greet/{name}")
    assert resp.status_code == 422


@pytest.mark.parametrize("x", [0, 2, -2, 1_000_000, -1_000_000])
def test_square(x):
    """Test the square endpoint with valid values."""
    resp = client.get(f"/math/square?x={x}")
    assert resp.status_code == 200
    assert resp.json() == {"x": x, "square": x * x}


@pytest.mark.parametrize("x", [1_000_001, -1_000_001])
def test_square_out_of_bounds(x):
    """Test the square endpoint with out-of-bounds values (should 422)."""
    resp = client.get(f"/math/square?x={x}")
    assert resp.status_code == 422


def test_create_user_success():
    """Test creating a user successfully."""
    payload = {"name": "Pandi", "email": "pandi@example.com", "age": 30}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["name"] == "Pandi"
    assert data["email"] == "pandi@example.com"
    # Age is not in output


def test_create_user_duplicate_email():
    """Test creating a user with a duplicate email (should 409)."""
    payload = {"name": "Pandi", "email": "pandi@example.com", "age": 30}
    client.post("/users", json=payload)
    resp = client.post("/users", json=payload)
    assert resp.status_code == 409
    assert resp.json()["detail"] == "Email already exists"


def test_create_user_invalid_email():
    """Test creating a user with an invalid email (should 422)."""
    payload = {"name": "Pandi", "email": "not-an-email", "age": 30}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 422


def test_create_user_missing_name():
    """Test creating a user with a missing name (should 422)."""
    payload = {"email": "pandi@example.com", "age": 30}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 422


def test_get_user_success():
    """Test retrieving a user by ID successfully."""
    payload = {"name": "Pandi", "email": "pandi@example.com", "age": 30}
    post_resp = client.post("/users", json=payload)
    user_id = post_resp.json()["id"]
    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_id
    assert data["name"] == "Pandi"
    assert data["email"] == "pandi@example.com"


def test_get_user_not_found():
    """Test retrieving a user with a non-existent ID (should 404)."""
    resp = client.get("/users/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"


def test_get_user_invalid_id():
    """Test retrieving a user with an invalid ID (should 422)."""
    resp = client.get("/users/0")
    assert resp.status_code == 422
