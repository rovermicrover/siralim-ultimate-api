from app.routers.classes import SortingSchema
from typing import List, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import contains_eager, aliased
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.orm.race import RaceOrm
from app.orm.klass import KlassOrm
from app.models.race import RaceModel
from .helpers import (
    PaginationSchema,
    build_sorting_schema,
    select,
    has_session,
    has_pagination,
    has_sorting,
)

router = APIRouter(
    prefix="/races",
    tags=["races"],
)

SortingSchema = build_sorting_schema(
    [
        RaceOrm.id,
        RaceOrm.name,
        RaceOrm.default_klass_id,
    ]
)

EAGER_LOAD_OPTIONS = [contains_eager(RaceOrm.default_klass)]


class IndexSchema(BaseModel):
    data: List[RaceModel]
    pagination: PaginationSchema
    sorting: SortingSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingSchema, "id")


@router.get("/", response_model=IndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationSchema = Depends(pagination_depend),
    sorting: SortingSchema = Depends(sorting_depend),
):
    races_orm = (
        select(RaceOrm)
        .join(KlassOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    races_model = RaceModel.from_orm_list(races_orm)
    return IndexSchema(
        data=races_model, pagination=pagination, sorting=SortingSchema
    )


class GetSchema(BaseModel):
    data: RaceModel


@router.get("/{race_id}", response_model=GetSchema)
def get(race_id: str, session=Depends(has_session)):
    races_orm = (
        select(RaceOrm)
        .join(KlassOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .where(RaceOrm.where_slug_or_id(race_id))
        .get_scalar(session)
    )
    races_model = RaceModel.from_orm(races_orm)
    return GetSchema(data=races_model)
