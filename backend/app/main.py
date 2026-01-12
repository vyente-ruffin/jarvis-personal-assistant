"""JARVIS FastAPI Application - Main Entry Point."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown events."""
    # Startup
    logger.info("Starting JARVIS...")
    logger.info(f"Memory API URL: {settings.mem0_api_url}")
    logger.info(f"User ID: {settings.user_id}")

    # Initialize Azure Application Insights if configured
    if settings.applicationinsights_connection_string:
        logger.info("Azure Application Insights configured")

    yield

    # Shutdown
    logger.info("Shutting down JARVIS...")


app = FastAPI(
    title="JARVIS",
    description="Personal AI Voice Assistant with Persistent Memory",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "JARVIS",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Detailed health check for Azure Container Apps."""
    return {
        "status": "healthy",
        "memory_api": settings.mem0_api_url,
        "user_id": settings.user_id,
    }


# TODO: Add WebSocket endpoint for voice streaming (M1.2)
# TODO: Add voice loop integration (M1.3)
# TODO: Add memory routes (M1.4)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
