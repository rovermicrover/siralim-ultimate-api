from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.orm.perk import PerkOrm
from app.models.perk import PerkModel
from app.orm.specialization import SpecializationOrm
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
    prefix="/perks",
    tags=["perks"],
)

SORTING_FILTER_FIELDS = [
    PerkOrm.id,
    PerkOrm.name,
    PerkOrm.ranks,
    PerkOrm.cost,
    PerkOrm.annointment,
    PerkOrm.ascension,
    PerkOrm.specialization_id,
    PerkOrm.specialization_name,
    PerkOrm.tags,
    PerkOrm.full_text,
]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "Perk", SORTING_FILTER_FIELDS
)

EAGER_LOAD_OPTIONS = [
    contains_eager(PerkOrm.specialization),
]


class PerksIndexSchema(BaseModel):
    data: List[PerkModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingRequestSchema)


@router.get("", response_model=PerksIndexSchema, include_in_schema=False)
@router.get("/", response_model=PerksIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    perks_count = select(func.count(PerkOrm.id.distinct())).get_scalar(session)
    perks_orm = (
        select(PerkOrm)
        .join(SpecializationOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    perks_model = PerkModel.from_orm_list(perks_orm)
    return PerksIndexSchema(
        data=perks_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, perks_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("Perk", SORTING_FILTER_FIELDS)


class PerksSearchSchema(BaseModel):
    data: List[PerkModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class PerksSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema()
    sorting: Optional[SortingRequestSchema] = SortingRequestSchema()


@router.post("/search", response_model=PerksSearchSchema)
def search(search: PerksSearchRequest, session=Depends(has_session)):
    perks_count = (
        select(func.count(PerkOrm.id.distinct()))
        .filters(search.filter.filters)
        .join(SpecializationOrm)
        .get_scalar(session)
    )
    perks_orm = (
        select(PerkOrm)
        .filters(search.filter.filters)
        .join(SpecializationOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    perks_model = PerkModel.from_orm_list(perks_orm)
    return PerksSearchSchema(
        data=perks_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, perks_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class PerksGetSchema(BaseModel):
    data: PerkModel


@router.get("/{perk_id}", response_model=PerksGetSchema)
def get(perk_id: str, session=Depends(has_session)):
    perk_orm = (
        select(PerkOrm)
        .join(SpecializationOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .where(PerkOrm.where_slug_or_id(perk_id))
        .get_scalar(session)
    )
    perk_model = PerkModel.from_orm(perk_orm)
    return PerksGetSchema(data=perk_model)
