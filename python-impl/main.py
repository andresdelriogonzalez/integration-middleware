from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime, timezone

app = FastAPI()

sync_records = {}
next_sync_id = {"value": 1}

SOURCE_URL = "http://localhost:8001"
TARGET_URL = "http://localhost:8002"

class SyncRequest(BaseModel):
    source_customer_id: int

@app.post("/sync/customers", status_code=201)
def sync_customer(req: SyncRequest):
    source_resp = requests.get(f"{SOURCE_URL}/customers/{req.source_customer_id}")
    if source_resp.status_code == 404:
        raise HTTPException(status_code=404, detail="source customer not found")
    customer = source_resp.json()

    target_resp = requests.post(f"{TARGET_URL}/customers", json=customer)
    if target_resp.status_code >= 500:
        raise HTTPException(status_code=502, detail="target system error")
    target_data = target_resp.json()

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

