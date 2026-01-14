from fastapi import APIRouter, UploadFile, File, HTTPException
import json
from state.customer_store import add_customer, load_customers
from state.purchase_store import add_purchase, load_purchases

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/customers")
async def ingest_customers(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files allowed")

    data = json.loads(await file.read())

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Expected list of customers")

    for customer in data:
        add_customer(customer)

    load_customers()  # refresh store
    return {"status": "success", "ingested": len(data)}


@router.post("/purchases")
async def ingest_purchases(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files allowed")

    data = json.loads(await file.read())

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Expected list of purchases")

    for purchase in data:
        add_purchase(purchase)

    load_purchases()
    return {"status": "success", "ingested": len(data)}
from fastapi import APIRouter, UploadFile, File, HTTPException
import json
from state.customer_store import add_customer, load_customers
from state.purchase_store import add_purchase, load_purchases

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/customers")
async def ingest_customers(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files allowed")

    data = json.loads(await file.read())

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Expected list of customers")

    for customer in data:
        add_customer(customer)

    load_customers()  # refresh store
    return {"status": "success", "ingested": len(data)}


@router.post("/purchases")
async def ingest_purchases(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files allowed")

    data = json.loads(await file.read())

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Expected list of purchases")

    for purchase in data:
        add_purchase(purchase)

    load_purchases()
    return {"status": "success", "ingested": len(data)}
