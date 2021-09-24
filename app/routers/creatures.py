from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import contains_eager, selectinload
from sqlalchemy import func

from app.orm.creature import CreatureOrm
from app.models.creature import CreatureModel
from app.orm.klass import KlassOrm
from app.orm.race import RaceOrm
from app.orm.trait import TraitOrm
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
    prefix="/creatures",
    tags=["creatures"],
)

SORTING_FILTER_FIELDS = [
    CreatureOrm.id,
    CreatureOrm.name,
    CreatureOrm.health,
    CreatureOrm.attack,
    CreatureOrm.intelligence,
    CreatureOrm.defense,
    CreatureOrm.speed,
    CreatureOrm.klass_id,
    CreatureOrm.klass_name,
    CreatureOrm.race_id,
    CreatureOrm.race_name,
    CreatureOrm.trait_id,
    CreatureOrm.trait_name,
    CreatureOrm.trait_tags,
]

SortingRequestSchema, SortingResponseSchema = build_sorting_schema(
    "Creature", SORTING_FILTER_FIELDS
)

EAGER_LOAD_OPTIONS = (
    contains_eager(CreatureOrm.klass),
    contains_eager(CreatureOrm.race),
    contains_eager(CreatureOrm.trait),
    selectinload(CreatureOrm.race, RaceOrm.default_klass),
    selectinload(CreatureOrm.sources),
)


class CreaturesIndexSchema(BaseModel):
    data: List[CreatureModel]
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SortingRequestSchema)


@router.get("", response_model=CreaturesIndexSchema, include_in_schema=False)
@router.get("/", response_model=CreaturesIndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationRequestSchema = Depends(pagination_depend),
    sorting: SortingRequestSchema = Depends(sorting_depend),
):
    creatures_count = select(func.count(CreatureOrm.id.distinct())).get_scalar(
        session
    )
    creatures_orm = (
        select(CreatureOrm)
        .join(RaceOrm)
        .join(KlassOrm, CreatureOrm.klass_id == KlassOrm.id)
        .join(TraitOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    creatures_model = CreatureModel.from_orm_list(creatures_orm)
    return CreaturesIndexSchema(
        data=creatures_model,
        pagination=PaginationResponseSchema.from_request(
            pagination, creatures_count
        ),
        sorting=SortingResponseSchema.from_orm(sorting),
    )


FilterSchema = build_filtering_schema("Creature", SORTING_FILTER_FIELDS)


class CreaturesSearchSchema(BaseModel):
    data: List[CreatureModel]
    filter: FilterSchema
    pagination: PaginationResponseSchema
    sorting: SortingResponseSchema


class CreaturesSearchRequest(BaseModel):
    filter: FilterSchema
    pagination: Optional[PaginationRequestSchema] = PaginationRequestSchema()
    sorting: Optional[SortingRequestSchema] = SortingRequestSchema()


@router.post("/search", response_model=CreaturesSearchSchema)
def search(search: CreaturesSearchRequest, session=Depends(has_session)):
    creatures_count = (
        select(func.count(CreatureOrm.id.distinct()))
        .filters(search.filter.filters)
        .join(RaceOrm)
        .join(KlassOrm, CreatureOrm.klass_id == KlassOrm.id)
        .join(TraitOrm)
        .get_scalar(session)
    )
    creatures_orm = (
        select(CreatureOrm)
        .filters(search.filter.filters)
        .join(RaceOrm)
        .join(KlassOrm, CreatureOrm.klass_id == KlassOrm.id)
        .join(TraitOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .pagination(search.pagination)
        .sorting(search.sorting)
        .get_scalars(session)
    )
    creatures_model = CreatureModel.from_orm_list(creatures_orm)
    return CreaturesSearchSchema(
        data=creatures_model,
        filter=search.filter,
        pagination=PaginationResponseSchema.from_request(
            search.pagination, creatures_count
        ),
        sorting=SortingResponseSchema.from_orm(search.sorting),
    )


class CreaturesGetSchema(BaseModel):
    data: CreatureModel


@router.get("/{creature_id}", response_model=CreaturesGetSchema)
def get(creature_id: str, session=Depends(has_session)):
    creatures_orm = (
        select(CreatureOrm)
        .join(RaceOrm)
        .join(KlassOrm, CreatureOrm.klass_id == KlassOrm.id)
        .join(TraitOrm)
        .options(*EAGER_LOAD_OPTIONS)
        .where(CreatureOrm.where_slug_or_id(creature_id))
        .get_scalar(session)
    )
    creatures_model = CreatureModel.from_orm(creatures_orm)
    return CreaturesGetSchema(data=creatures_model)
