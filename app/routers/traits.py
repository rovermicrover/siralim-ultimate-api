from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.orm.trait import TraitOrm
from app.models.trait import TraitModel
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
    prefix="/traits",
    tags=["traits"],
)

SORTING_FILTER_FIELDS = [
    TraitOrm.id,
    TraitOrm.name,
    TraitOrm.material_name,
    TraitOrm.tags,
]

SortingSchema = build_sorting_schema(SORTING_FILTER_FIELDS)


class IndexSchema(BaseModel):
    data: List[TraitModel]
    pagination: PaginationSchema
    sorting: SortingSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingSchema)


@router.get("/", response_model=IndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationSchema = Depends(pagination_depend),
    sorting: SortingSchema = Depends(sorting_depend),
):
    traits_orm = (
        select(TraitOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    traits_model = TraitModel.from_orm_list(traits_orm)
    return IndexSchema(
        data=traits_model, pagination=pagination, sorting=sorting
    )


FilterSchema = build_filtering_schema(SORTING_FILTER_FIELDS)


class SearchSchema(BaseModel):
    data: List[TraitModel]
    filter: FilterSchema
    pagination: PaginationSchema
    sorting: SortingSchema


class SearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationSchema] = PaginationSchema()
    sorting: Optional[SortingSchema] = SortingSchema()


@router.post("/search", response_model=SearchSchema)
def search(search: SearchRequest, session=Depends(has_session)):
    traits_orm = (
        select(TraitOrm)
        .filters(search.filter.filters)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    traits_model = TraitModel.from_orm_list(traits_orm)
    return SearchSchema(
        data=traits_model,
        filter=search.filter,
        pagination=search.pagination,
        sorting=search.sorting,
    )


class GetSchema(BaseModel):
    data: TraitModel


@router.get("/{trait_id}", response_model=GetSchema)
def get(trait_id: str, session=Depends(has_session)):
    trait_orm = (
        select(TraitOrm)
        .where(TraitOrm.where_slug_or_id(trait_id))
        .get_scalar(session)
    )
    trait_model = TraitModel.from_orm(trait_orm)
    return GetSchema(data=trait_model)
