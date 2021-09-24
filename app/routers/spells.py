from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.orm.spell import SpellOrm
from app.models.spell import SpellModel
from app.orm.klass import KlassOrm
from app.orm.source import SourceOrm
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
    prefix="/spells",
    tags=["spells"],
)

SORTING_FILTER_FIELDS = [
    SpellOrm.id,
    SpellOrm.name,
    SpellOrm.charges,
    SpellOrm.klass_id,
    SpellOrm.klass_name,
    SpellOrm.source_id,
    SpellOrm.source_name,
    SpellOrm.tags,
]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "Spell", SORTING_FILTER_FIELDS
)

EAGER_LOAD_OPTIONS = [
    contains_eager(SpellOrm.klass),
    contains_eager(SpellOrm.source),
]


class SpellsIndexSchema(BaseModel):
    data: List[SpellModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingRequestSchema)


@router.get("", response_model=SpellsIndexSchema, include_in_schema=False)
@router.get("/", response_model=SpellsIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    spells_count = select(func.count(SpellOrm.id.distinct())).get_scalar(
        session
    )
    spells_orm = (
        select(SpellOrm)
        .join(KlassOrm)
        .join(SourceOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    spells_model = SpellModel.from_orm_list(spells_orm)
    return SpellsIndexSchema(
        data=spells_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, spells_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("Spell", SORTING_FILTER_FIELDS)


class SpellsSearchSchema(BaseModel):
    data: List[SpellModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class SpellsSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema()
    sorting: Optional[PaginationRequestSchema] = PaginationRequestSchema()


@router.post("/search", response_model=SpellsSearchSchema)
def search(search: SpellsSearchRequest, session=Depends(has_session)):
    spells_count = (
        select(func.count(SpellOrm.id.distinct()))
        .filters(search.filter.filters)
        .join(KlassOrm)
        .join(SourceOrm)
        .get_scalar(session)
    )
    spells_orm = (
        select(SpellOrm)
        .filters(search.filter.filters)
        .join(KlassOrm)
        .join(SourceOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    spells_model = SpellModel.from_orm_list(spells_orm)
    return SpellsSearchSchema(
        data=spells_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, spells_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class SpellsGetSchema(BaseModel):
    data: SpellModel


@router.get("/{spell_id}", response_model=SpellsGetSchema)
def get(spell_id: str, session=Depends(has_session)):
    spell_orm = (
        select(SpellOrm)
        .join(KlassOrm)
        .join(SourceOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .where(SpellOrm.where_slug_or_id(spell_id))
        .get_scalar(session)
    )
    spell_model = SpellModel.from_orm(spell_orm)
    return SpellsGetSchema(data=spell_model)
