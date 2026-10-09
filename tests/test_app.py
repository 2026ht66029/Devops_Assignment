"""Unit and API tests for the ACEest Flask application."""

from datetime import date

import pytest

from aceest import create_app
from aceest.fitness import calculate_bmi, check_membership


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Fitness and Gym" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {
        "service": "aceest-fitness-api",
        "status": "healthy",
        "version": "1.0.0",
    }


def test_program_catalog(client):
    payload = client.get("/api/programs").get_json()
    assert payload["count"] == 4
    assert "strength" in payload["programs"]


def test_program_lookup_accepts_spaces(client):
    response = client.get("/api/programs/weight%20loss")
    assert response.status_code == 200
    assert response.get_json()["goal"] == "weight-loss"


def test_unknown_program_returns_404(client):
    response = client.get("/api/programs/unknown")
    assert response.status_code == 404
    assert response.get_json()["status"] == "error"


def test_bmi_endpoint_returns_healthy_category(client):
    response = client.post("/api/bmi", json={"height_cm": 180, "weight_kg": 75})
    assert response.status_code == 200
    assert response.get_json()["bmi"] == 23.1
    assert response.get_json()["category"] == "healthy"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"height_cm": 0, "weight_kg": 70},
        {"height_cm": "tall", "weight_kg": 70},
    ],
)
def test_bmi_endpoint_rejects_invalid_values(client, payload):
    response = client.post("/api/bmi", json=payload)
    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_bmi_function_obesity_boundary():
    assert calculate_bmi(170, 87)["category"] == "obesity"


def test_membership_active_and_expired():
    today = date(2026, 10, 1)
    active = check_membership("2026-10-31", today=today)
    expired = check_membership("2026-09-30", today=today)
    assert active == {
        "expiry_date": "2026-10-31",
        "status": "active",
        "days_remaining": 30,
    }
    assert expired["status"] == "expired"
    assert expired["days_remaining"] == 0


def test_membership_endpoint_rejects_bad_date(client):
    response = client.post("/api/membership/check", json={"expiry_date": "01-10-2026"})
    assert response.status_code == 400
    assert "YYYY-MM-DD" in response.get_json()["message"]


def test_class_schedule(client):
    response = client.get("/api/classes")
    assert response.status_code == 200
    assert response.get_json()["count"] == 4
