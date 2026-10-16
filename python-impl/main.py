from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
from datetime import datetime, timezone
import time

app = FastAPI()

sync_records = {}
next_sync_id = {"value": 1}
idempotency_cache = {}

SOURCE_URL = "http://localhost:8001"
TARGET_URL = "http://localhost:8002"

class SyncRequest(BaseModel):
    source_customer_id: int

@app.post("/sync/customers", status_code=201)
def sync_customer(req: SyncRequest, idempotency_key: str | None = Header(None, alias="Idempotency-Key")):

    # Check idempotency cache
    if idempotency_key and idempotency_key in idempotency_cache:
        return idempotency_cache[idempotency_key]

    # Fetch from source system
    try:
        source_resp = requests.get(f"{SOURCE_URL}/customers/{req.source_customer_id}", timeout=10)
    except requests.HTTPException:
        raise HTTPException(status_code=503, detail="source system unreachable")

    if source_resp.status_code == 404:
        raise HTTPException(status_code=404, detail="source customer not found")
    if source_resp.status_code >= 400:
        raise HTTPException(status_code=502, detail="error response from source system")
    customer = source_resp.json()


    # Forward to target system with retries and exponential backoff
    headers = {}
    if idempotency_key:
        headers['Idempotency-Key'] = idempotency_key

    max_retries = 3
    target_resp = None
    for attempt in range(max_retries):
        try:
            target_resp = requests.post(f"{TARGET_URL}/customers", json=customer, headers=headers, timeout=10)
            if target_resp.status_code < 500:
                break
        except requests.HTTPException:
            # Network-level failure; will retry on next iteration
            pass
        time.sleep(2 ** attempt) #backoff: 1s, 2s, 4s
        
    if not target_resp or target_resp.status_code >= 500:
        raise HTTPException(status_code=502, detail="target system error after retries")
    target_data = target_resp.json()

    # Record successful sync
    sync_id = next_sync_id["value"]
    next_sync_id["value"] += 1
    record = {
        "id": sync_id,
        "source_customer_id": req.source_customer_id,
        "target_id": target_data["id"],
        "name": customer["name"],
        "email": customer["email"],
        "synced_at": datetime.now(timezone.utc).isoformat(),
    }
    sync_records[sync_id] = record
    if idempotency_key:
        idempotency_cache[idempotency_key] = record
    return record


@app.get("/sync/customers/{sync_id}")
def get_sync(sync_id: int):
    record = sync_records.get(sync_id)
    if not record:
        raise HTTPException(status_code = 404, detail= "sync record not found")
    return record

@app.get("/health")
def health():
    return {"status": "ok"}

