"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.logging import logger
from src.presentation.routes.usuarios_routes import router as usuarios_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    logger.info("FastAPI application starting")
    yield
    # Shutdown
    logger.info("FastAPI application shutting down")


app = FastAPI(
    title="PPP Expert IA",
    description="Sistema Inteligente para Elaboração de Perfil Profissiográfico Previdenciário",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    logger.info("Health check")
    return {"status": "ok", "version": "0.1.0"}


# Include routers
app.include_router(usuarios_router)
