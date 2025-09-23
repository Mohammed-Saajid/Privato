from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from privato.app.api.routes.api import router as api_router
import logging

logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
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

# Resolve the path relative to this file
static_dir = Path(__file__).parent / "static" / "dist"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
