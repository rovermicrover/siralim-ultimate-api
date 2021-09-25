from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func

from app.orm.trait import TraitOrm
from app.models.trait import TraitModel
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
    prefix="/traits",
    tags=["traits"],
)

SORTING_FILTER_FIELDS = [
    TraitOrm.id,
    TraitOrm.name,
    TraitOrm.material_name,
    TraitOrm.tags,
    TraitOrm.full_text,
]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "Trait", SORTING_FILTER_FIELDS
)


class TraitsIndexSchema(BaseModel):
    data: List[TraitModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingRequestSchema)


@router.get("", response_model=TraitsIndexSchema, include_in_schema=False)
@router.get("/", response_model=TraitsIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    traits_count = select(func.count(TraitOrm.id.distinct())).get_scalar(
        session
    )
    traits_orm = (
        select(TraitOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    traits_model = TraitModel.from_orm_list(traits_orm)
    return TraitsIndexSchema(
        data=traits_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, traits_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("Trait", SORTING_FILTER_FIELDS)


class TraitsSearchSchema(BaseModel):
    data: List[TraitModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class TraitsSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema()
    sorting: Optional[SortingRequestSchema] = SortingRequestSchema()


@router.post("/search", response_model=TraitsSearchSchema)
def search(search: TraitsSearchRequest, session=Depends(has_session)):
    traits_count = (
        select(func.count(TraitOrm.id.distinct()))
        .filters(search.filter.filters)
        .get_scalar(session)
    )
    traits_orm = (
        select(TraitOrm)
        .filters(search.filter.filters)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    traits_model = TraitModel.from_orm_list(traits_orm)
    return TraitsSearchSchema(
        data=traits_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, traits_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class TraitsGetSchema(BaseModel):
    data: TraitModel


@router.get("/{trait_id}", response_model=TraitsGetSchema)
def get(trait_id: str, session=Depends(has_session)):
    trait_orm = (
        select(TraitOrm)
        .where(TraitOrm.where_slug_or_id(trait_id))
        .get_scalar(session)
    )
    trait_model = TraitModel.from_orm(trait_orm)
    return TraitsGetSchema(data=trait_model)
