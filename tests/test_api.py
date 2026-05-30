from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Azure Smart Notifier is running"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_send_notification():
    response = client.post("/notify", json={
        "message": "Test alert",
        "recipient": "test@company.com",
        "priority": "normal"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "queued"


def test_empty_message():
    response = client.post("/notify", json={
        "message": "",
        "recipient": "test@company.com"
    })
    assert response.status_code == 400