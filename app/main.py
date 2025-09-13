"""Main package for the app module."""
from fastapi import FastAPI
from app.api.routes.api import router as api_router

app = FastAPI()
app.include_router(api_router)
