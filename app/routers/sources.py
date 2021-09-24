from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from app.orm.source import SourceOrm
from app.models.source import SourceModel
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
    prefix="/sources",
    tags=["sources"],
)

SORTING_FILTER_FIELDS = [
    SourceOrm.id,
    SourceOrm.name,
]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "Source", SORTING_FILTER_FIELDS
)


class SourcesIndexSchema(BaseModel):
    data: List[SourceModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingRequestSchema)


@router.get("", response_model=SourcesIndexSchema, include_in_schema=False)
@router.get("/", response_model=SourcesIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    sources_count = select(func.count(SourceOrm.id.distinct())).get_scalar(
        session
    )
    sources_orm = (
        select(SourceOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    sources_model = SourceModel.from_orm_list(sources_orm)
    return SourcesIndexSchema(
        data=sources_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, sources_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("Source", SORTING_FILTER_FIELDS)


class SourcesSearchSchema(BaseModel):
    data: List[SourceModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class SourcesSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema()
    sorting: Optional[PaginationRequestSchema] = PaginationRequestSchema()


@router.post("/search", response_model=SourcesSearchSchema)
def search(search: SourcesSearchRequest, session=Depends(has_session)):
    soures_count = (
        select(func.count(SourceOrm.id.distinct()))
        .filters(search.filter.filters)
        .get_scalar(session)
    )
    soures_orm = (
        select(SourceOrm)
        .filters(search.filter.filters)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    soures_model = SourceModel.from_orm_list(soures_orm)
    return SourcesSearchSchema(
        data=soures_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, soures_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class SourcesGetSchema(BaseModel):
    data: SourceModel


@router.get("/{source_id}", response_model=SourcesGetSchema)
def get(source_id: str, session=Depends(has_session)):
    source_orm = (
        select(SourceOrm)
        .where(SourceOrm.where_slug_or_id(source_id))
        .get_scalar(session)
    )
    source_model = SourceModel.from_orm(source_orm)
    return SourcesGetSchema(data=source_model)
