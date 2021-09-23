from app.routers.classes import SortingSchema
from typing import List, Dict, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import contains_eager

from app.orm.race import RaceOrm
from app.orm.klass import KlassOrm
from app.models.race import RaceModel
from .helpers import (
    PaginationRequestSchema,
    PaginationResponseSchema,
    build_sorting_schema,
    build_filtering_schema,
    select,
    has_session,
    has_pagination,
    has_sorting,
)

router = APIRouter(
    prefix="/races",
    tags=["races"],
)

SORTING_FILTER_FIELDS = [
    RaceOrm.id,
    RaceOrm.name,
    RaceOrm.default_klass_id,
    RaceOrm.default_klass_name,
]

SortingSchema = build_sorting_schema(SORTING_FILTER_FIELDS)

EAGER_LOAD_OPTIONS = [contains_eager(RaceOrm.default_klass)]


class IndexSchema(BaseModel):
    data: List[RaceModel]
    pagination: PaginationResponseSchema
    sorting: SortingSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingSchema)


@router.get("", response_model=IndexSchema, include_in_schema=False)
@router.get("/", response_model=IndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingSchema = Depends(sorting_depend),
):
    races_count = select(func.count(RaceOrm.id.distinct())).get_scalar(session)
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
        data=races_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, races_count
        ),
        sorting=sorting,
    )


FilterSchema = build_filtering_schema(SORTING_FILTER_FIELDS)


class SearchSchema(BaseModel):
    data: List[RaceModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingSchema


class SearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema()
    sorting: Optional[SortingSchema] = SortingSchema()


@router.post("/search", response_model=SearchSchema)
def search(search: SearchRequest, session=Depends(has_session)):
    races_count = (
        select(func.count(RaceOrm.id.distinct()))
        .filters(search.filter.filters)
        .join(KlassOrm)
        .get_scalar(session)
    )
    races_orm = (
        select(RaceOrm)
        .filters(search.filter.filters)
        .join(KlassOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    races_model = RaceModel.from_orm_list(races_orm)
    return SearchSchema(
        data=races_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, races_count
        ),
        sorting=search.sorting,
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
