from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.orm.source import SourceOrm
from app.models.source import SourceModel
from .helpers import (
    PaginationSchema,
    build_sorting_schema,
    build_filtering_schema,
    select,
    has_session,
    has_pagination,
    has_sorting,
)

router = APIRouter(
    prefix="/sources",
    tags=["sources"],
)

SORTING_FILTER_FIELDS = [
    SourceOrm.id,
    SourceOrm.name,
]

SortingSchema = build_sorting_schema(SORTING_FILTER_FIELDS)


class IndexSchema(BaseModel):
    data: List[SourceModel]
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
    sources_orm = (
        select(SourceOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    sources_model = SourceModel.from_orm_list(sources_orm)
    return IndexSchema(
        data=sources_model, pagination=pagination, sorting=sorting
    )

FilterSchema = build_filtering_schema(SORTING_FILTER_FIELDS)


class SearchSchema(BaseModel):
    data: List[SourceModel]
    filter: FilterSchema
    pagination: PaginationSchema
    sorting: SortingSchema


class SearchRequest(BaseModel):
    filter: FilterSchema
    pagination: PaginationSchema
    sorting: SortingSchema


@router.post("/search", response_model=SearchSchema)
def search(search: SearchRequest, session=Depends(has_session)):
    soures_orm = (
        select(SourceOrm)
        .filters(search.filter.filters)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    soures_model = SourceModel.from_orm_list(soures_orm)
    return SearchSchema(
        data=soures_model,
        filter=search.filter,
        pagination=search.pagination,
        sorting=search.sorting,
    )



class GetSchema(BaseModel):
    data: SourceModel


@router.get("/{source_id}", response_model=GetSchema)
def get(source_id: str, session=Depends(has_session)):
    source_orm = (
        select(SourceOrm)
        .where(SourceOrm.where_slug_or_id(source_id))
        .get_scalar(session)
    )
    source_model = SourceModel.from_orm(source_orm)
    return GetSchema(data=source_model)
