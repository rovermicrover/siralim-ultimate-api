from fastapi import FastAPI
from pydantic.main import BaseModel

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
