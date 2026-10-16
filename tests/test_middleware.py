import requests

BASE_URL = "http://localhost:8096"


def test_sync_creates_customer_in_target():
    response = requests.post(
        f"{BASE_URL}/sync/customers",
        json={"source_customer_id": 1},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Andrés Del Río"
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

def test_sync_same_customer_same_idempotency_key():
    response1 = requests.post(
        f"{BASE_URL}/sync/customers",
        json={"source_customer_id": 1},
        headers={"Idempotency-Key": "abc-234"}
    )
    sync_id1 = response1.json()["id"]

    response2 = requests.post(
        f"{BASE_URL}/sync/customers",
        json={"source_customer_id": 1},
        headers={"Idempotency-Key": "abc-234"}
    )
    sync_id2 = response2.json()["id"]

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert sync_id1 == sync_id2
