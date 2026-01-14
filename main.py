# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv



# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# Create FastAPI app (THIS is the ASGI app)
# -------------------------------------------------
app = FastAPI(
    title="AI Loyalty Platform",
    description="Agentic AI-powered loyalty & campaign intelligence system",
    version="1.0.0",
)

# -------------------------------------------------
# CORS (Frontend Integration)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # demo-safe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# State loading (snapshot → memory)
# -------------------------------------------------
from state.customer_store import load_customers
from state.purchase_store import load_purchases


@app.on_event("startup")
def startup_event():
    customers = load_customers()
    purchases = load_purchases()

    print(f"[STARTUP] Loaded {len(customers)} customers")
    print(f"[STARTUP] Loaded {len(purchases)} purchases")


# -------------------------------------------------
# API Routers
# -------------------------------------------------
from api.routes.customers import router as customer_router
from api.routes.purchases import router as purchase_router
from api.routes.ai_module import router as ai_router
from api.routes.campaigns import router as campaign_router
from api.routes.ingestion import router as ingestion_router

app.include_router(customer_router)
app.include_router(purchase_router)
app.include_router(ai_router)
app.include_router(campaign_router)
app.include_router(ingestion_router)

# -------------------------------------------------
# Health Check
# -------------------------------------------------
@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "AI Loyalty Platform",
        "version": "1.0.0",
    }
