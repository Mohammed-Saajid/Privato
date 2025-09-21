"""Main package for the app module."""
from fastapi import FastAPI
from app.api.routes.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)

origins = [
    "http://localhost",
    "http://localhost:5173",
]


app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)