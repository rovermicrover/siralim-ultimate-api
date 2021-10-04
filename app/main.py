import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic.main import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from .middleware import content_policy, not_found

from .routers import (
    classes,
    creatures,
    perks,
    races,
    sources,
    specializations,
    spells,
    traits,
    status_effects,
)

logging.basicConfig()
logging.getLogger("sqlalchemy").setLevel(logging.INFO)

app = FastAPI()

allow_origins = os.environ.get("ALLOW_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Authorization",
        "Accept",
        "Accept-Encoding",
        "Accept-Language",
        "Cache-Control",
        "Connection",
        "Cookie",
        "Host",
        "Upgrade-Insecure-Requests",
        "User-Agent",
    ],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=content_policy)
app.add_middleware(BaseHTTPMiddleware, dispatch=not_found)

app.include_router(classes.router)
app.include_router(creatures.router)
app.include_router(perks.router)
app.include_router(races.router)
app.include_router(sources.router)
app.include_router(specializations.router)
app.include_router(spells.router)
app.include_router(status_effects.router)
app.include_router(traits.router)


class HealthCheckSchema(BaseModel):
    healthcheck: bool


class RootSchema(BaseModel):
    data: HealthCheckSchema


@app.get("/", response_model=RootSchema)
async def root():
    return {"data": {"healthcheck": True}}
