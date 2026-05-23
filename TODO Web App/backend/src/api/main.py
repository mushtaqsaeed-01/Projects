"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import tasks

app = FastAPI(
    title="TODO Application API",
    description="REST API for managing TODO tasks",
    version="1.0.0"
)

# Configure CORS to allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(tasks.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "TODO Application API", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
