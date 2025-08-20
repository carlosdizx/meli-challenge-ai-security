from fastapi import FastAPI
from data.routers.health import router as health_router
from data.routers.analyze import router as analyze_router

app = FastAPI(title="Security and AI for Risk-Based Authentication", version="1.0.0")

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(analyze_router, prefix="/analyze", tags=["analyze"])
