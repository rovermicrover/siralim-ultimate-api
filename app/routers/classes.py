from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func

from app.orm.klass import KlassOrm
from app.models.klass import KlassModel
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
    prefix="/classes",
    tags=["classes"],
)

DEFAULT_PAGE_SIZE = 5

SORTING_FILTER_FIELDS = [KlassOrm.id, KlassOrm.name]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "Klass", SORTING_FILTER_FIELDS
)


class KlassesIndexSchema(BaseModel):
    data: List[KlassModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination(default_size=DEFAULT_PAGE_SIZE)
sorting_depend = has_sorting(SortingRequestSchema)


@router.get("", response_model=KlassesIndexSchema, include_in_schema=False)
@router.get("/", response_model=KlassesIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    klasses_count = select(func.count(KlassOrm.id.distinct())).get_scalar(
        session
    )
    klasses_orm = (
        select(KlassOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    klasses_model = KlassModel.from_orm_list(klasses_orm)
    return KlassesIndexSchema(
        data=klasses_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, klasses_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("Klass", SORTING_FILTER_FIELDS)


class KlassesSearchSchema(BaseModel):
    data: List[KlassModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class KlassesSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema(
        size=DEFAULT_PAGE_SIZE
    )
    sorting: Optional[SortingRequestSchema] = SortingRequestSchema()


@router.post("/search", response_model=KlassesSearchSchema)
def search(search: KlassesSearchRequest, session=Depends(has_session)):
    klasses_count = (
        select(func.count(KlassOrm.id.distinct()))
        .filters(search.filter.filters)
        .get_scalar(session)
    )
    klasses_orm = (
        select(KlassOrm)
        .filters(search.filter.filters)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    klasses_model = KlassModel.from_orm_list(klasses_orm)
    return KlassesSearchSchema(
        data=klasses_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, klasses_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class KlassesGetSchema(BaseModel):
    data: KlassModel


@router.get("/{klass_id}", response_model=KlassesGetSchema)
def get(klass_id: str, session=Depends(has_session)):
    klasses_orm = (
        select(KlassOrm)
        .where(KlassOrm.where_slug_or_id(klass_id))
        .get_scalar(session)
    )
    klasses_model = KlassModel.from_orm(klasses_orm)
    return KlassesGetSchema(data=klasses_model)
