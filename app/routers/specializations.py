from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func

from app.orm.specialization import SpecializationOrm
from app.models.specialization import SpecializationModel
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
    prefix="/specializations",
    tags=["specializations"],
)

DEFAULT_PAGE_SIZE = 30

SORTING_FILTER_FIELDS = [SpecializationOrm.id, SpecializationOrm.name]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "Specialization", SORTING_FILTER_FIELDS
)


class SpecializationsIndexSchema(BaseModel):
    data: List[SpecializationModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination(default_size=DEFAULT_PAGE_SIZE)
sorting_depend = has_sorting(SortingRequestSchema)


@router.get(
    "", response_model=SpecializationsIndexSchema, include_in_schema=False
)
@router.get("/", response_model=SpecializationsIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    specializations_count = select(
        func.count(SpecializationOrm.id.distinct())
    ).get_scalar(session)
    specializations_orm = (
        select(SpecializationOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    specializations_model = SpecializationModel.from_orm_list(
        specializations_orm
    )
    return SpecializationsIndexSchema(
        data=specializations_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, specializations_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("Specialization", SORTING_FILTER_FIELDS)


class SpecializationsSearchSchema(BaseModel):
    data: List[SpecializationModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class SpecializationsSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema(
        size=DEFAULT_PAGE_SIZE
    )
    sorting: Optional[SortingRequestSchema] = SortingRequestSchema()


@router.post("/search", response_model=SpecializationsSearchSchema)
def search(search: SpecializationsSearchRequest, session=Depends(has_session)):
    specializations_count = (
        select(func.count(SpecializationOrm.id.distinct()))
        .filters(search.filter.filters)
        .get_scalar(session)
    )
    specializations_orm = (
        select(SpecializationOrm)
        .filters(search.filter.filters)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    specializations_model = SpecializationModel.from_orm_list(
        specializations_orm
    )
    return SpecializationsSearchSchema(
        data=specializations_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, specializations_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class SpecializationsGetSchema(BaseModel):
    data: SpecializationModel


@router.get("/{specialization_id}", response_model=SpecializationsGetSchema)
def get(specialization_id: str, session=Depends(has_session)):
    specialization_orm = (
        select(SpecializationOrm)
        .where(SpecializationOrm.where_slug_or_id(specialization_id))
        .get_scalar(session)
    )
    specialization_model = SpecializationModel.from_orm(specialization_orm)
    return SpecializationsGetSchema(data=specialization_model)
