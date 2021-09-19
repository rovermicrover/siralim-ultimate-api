import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic.main import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from .middleware.content_policy import content_policy

from .routers import (
    classes,
    creatures,
    races,
    sources,
    spells,
    traits,
    status_effects,
)

app = FastAPI()

allow_origins = os.environ.get('ALLOW_ORIGINS', '').split(',')

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

app.include_router(classes.router)
app.include_router(creatures.router)
app.include_router(races.router)
app.include_router(sources.router)
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
