import requests

BASE_URL = "http://localhost:8003"


def test_sync_creates_customer_in_target():
    response = requests.post(
        f"{BASE_URL}/sync/customers",
        json={"source_customer_id": 1},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Andres Del Rio"
    assert body["email"] == "andres@example.com"
    assert "target_id" in body


def test_sync_unknown_source_customer_returns_404():
    response = requests.post(
        f"{BASE_URL}/sync/customers",
        json={"source_customer_id": 999},
    )
    assert response.status_code == 404


def test_get_sync_status_after_creating():
    create = requests.post(
        f"{BASE_URL}/sync/customers",
        json={"source_customer_id": 2},
    )
    sync_id = create.json()["id"]

    status = requests.get(f"{BASE_URL}/sync/customers/{sync_id}")
    assert status.status_code == 200
    assert status.json()["source_customer_id"] == 2