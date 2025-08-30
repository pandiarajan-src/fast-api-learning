"""Unit tests for FastAPI endpoints in week1_day2.app.main."""

from fastapi.testclient import TestClient
from week1_day2.app.main import app

client = TestClient(app)


def test_get_item_ok():
    """Test getting an item with a valid ID returns correct response."""
    r = client.get("/items/10")
    assert r.status_code == 200
    assert r.json() == {"item_id": 10}


def test_get_item_bounds():
    """Test item endpoint with out-of-bounds IDs returns 422."""
    assert client.get("/items/0").status_code == 422
    assert client.get("/items/1000001").status_code == 422


def test_search_list_and_bool():
    """Test search endpoint with list and boolean query parameters."""
    r = client.get("/search", params={"query": "book", "tags": ["a", "b"], "exact": True})
    assert r.status_code == 200
    assert r.json() == {"q": "book", "tags": ["a", "b"], "exact": True}


def test_enum_category():
    """Test catalog endpoint with valid and invalid enum values."""
    assert client.get("/categories/electronics").status_code == 200
    assert client.get("/categories/food").status_code == 422  # invalid enum
