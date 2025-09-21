"""API routes module."""
from fastapi import APIRouter
from privato.app.api.routes import redactor
from privato.app.api.routes import analyzer
from privato.core.config import logger



logger.info("API routes module loaded successfully.")
router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}}
    )
router.include_router(redactor.router, tags=["redactor"], prefix="/v1")
router.include_router(analyzer.router, tags=["analyzer"], prefix="/v1")