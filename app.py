"""
app.py — FastAPI entry point for RetailIQ.
Run with: python app.py  OR  uvicorn app:app --reload --port 8000
"""
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

from backend.database import init_db
from backend.routes import query, alerts, analytics

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database on startup."""
    init_db()
    yield


app = FastAPI(
    title="RetailIQ – AI Retail Inventory & Sales Copilot",
    version="1.0.0",
    description="Natural language queries over your retail sales & inventory data, grounded in real numbers.",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API Routes ────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"], summary="API Health Check")
def health_check():
    return {"status": "healthy", "service": "RetailIQ API", "version": "1.0.0"}

app.include_router(query.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

# ── Serve React frontend (production build) ───────────────────────────────────
DIST = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.isdir(DIST):
    app.mount("/", StaticFiles(directory=DIST, html=True), name="frontend")
else:
    @app.get("/", include_in_schema=False)
    def root():
        return {"message": "RetailIQ API running. Frontend not built yet — run: cd frontend && npm run build"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
