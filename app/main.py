"""
FastAPI entry point.
"""

from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Context Engine API",
    description="Deterministic Context Awareness Engine for Automotive AI Systems",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Context Engine API is running"}