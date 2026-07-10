"""FastAPI application entry point."""

from fastapi import FastAPI
from src.core.logging import logger
from src.presentation.routes.usuarios_routes import router as usuarios_router

app = FastAPI(
    title="PPP Expert IA",
    description="Sistema Inteligente para Elaboração de Perfil Profissiográfico Previdenciário",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("FastAPI application starting")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("FastAPI application shutting down")


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    logger.info("Health check")
    return {"status": "ok", "version": "0.1.0"}


# Include routers
app.include_router(usuarios_router)
