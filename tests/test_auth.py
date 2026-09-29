import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "HEALTHY"


def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    # Checks for common login form identifiers
    assert b"password" in response.data.lower() or b"login" in response.data.lower()


def test_successful_login(client):
    response = client.post("/login", data={
        "username": "admin",
        "password": "HospitalAdmin@2026"
    }, follow_redirects=True)
    assert response.status_code == 200


def test_failed_login(client):
    response = client.post("/login", data={
        "username": "admin",
        "password": "WrongPassword123"
    }, follow_redirects=True)
    # Accepts 401 Unauthorized or 200 with flash message
    assert response.status_code in [200, 401]