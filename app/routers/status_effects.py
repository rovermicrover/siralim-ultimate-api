from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func

from app.orm.status_effect import StatusEffectOrm
from app.models.status_effect import StatusEffectModel
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
    prefix="/status-effects",
    tags=["status-effects"],
)

SORTING_FILTER_FIELDS = [
    StatusEffectOrm.id,
    StatusEffectOrm.name,
    StatusEffectOrm.category,
    StatusEffectOrm.turns,
    StatusEffectOrm.leave_chance,
    StatusEffectOrm.max_stacks,
    StatusEffectOrm.full_text,
]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "StatusEffet", SORTING_FILTER_FIELDS
)


class StatusEffectsIndexSchema(BaseModel):
    data: List[StatusEffectModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingRequestSchema)


@router.get(
    "", response_model=StatusEffectsIndexSchema, include_in_schema=False
)
@router.get("/", response_model=StatusEffectsIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    status_effects_count = select(
        func.count(StatusEffectOrm.id.distinct())
    ).get_scalar(session)
    status_effects_orm = (
        select(StatusEffectOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    status_effects_model = StatusEffectModel.from_orm_list(status_effects_orm)
    return StatusEffectsIndexSchema(
        data=status_effects_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, status_effects_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("StatusEffect", SORTING_FILTER_FIELDS)


class StatusEffectsSearchSchema(BaseModel):
    data: List[StatusEffectModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class StatusEffectsSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema()
    sorting: Optional[SortingRequestSchema] = SortingRequestSchema()


@router.post("/search", response_model=StatusEffectsSearchSchema)
def search(search: StatusEffectsSearchRequest, session=Depends(has_session)):
    status_effects_count = (
        select(func.count(StatusEffectOrm.id.distinct()))
        .filters(search.filter.filters)
        .get_scalar(session)
    )
    status_effects_orm = (
        select(StatusEffectOrm)
        .filters(search.filter.filters)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    status_effects_model = StatusEffectModel.from_orm_list(status_effects_orm)
    return StatusEffectsSearchSchema(
        data=status_effects_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, status_effects_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class StatusEffectsGetSchema(BaseModel):
    data: StatusEffectModel


@router.get("/{status_effect_id}", response_model=StatusEffectsGetSchema)
def get(status_effect_id: str, session=Depends(has_session)):
    status_effect_orm = (
        select(StatusEffectOrm)
        .where(StatusEffectOrm.where_slug_or_id(status_effect_id))
        .get_scalar(session)
    )
    status_effect_model = StatusEffectModel.from_orm(status_effect_orm)
    return StatusEffectsGetSchema(data=status_effect_model)
