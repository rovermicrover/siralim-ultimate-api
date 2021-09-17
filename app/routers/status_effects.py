from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .helpers import (
    PaginationSchema,
    SortingSchema,
    select,
    has_session,
    has_pagination,
    has_sorting,
)
from app.orm.status_effect import StatusEffectOrm
from app.models.status_effect import StatusEffectModel

router = APIRouter(
    prefix="/status-effects",
    tags=["status-effects"],
)

SORTABLES: Dict[str, InstrumentedAttribute] = {
    "id": StatusEffectOrm.id,
    "name": StatusEffectOrm.name,
    "category": StatusEffectOrm.category,
    "turns": StatusEffectOrm.turns,
    "leave_chance": StatusEffectOrm.leave_chance,
    "max_stacks": StatusEffectOrm.max_stacks,
}


class IndexSchema(BaseModel):
    data: List[StatusEffectModel]
    pagination: PaginationSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SORTABLES, "id")


@router.get("/", response_model=IndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationSchema = Depends(pagination_depend),
    sorting: SortingSchema = Depends(sorting_depend),
):
    status_effects_orm = (
        select(StatusEffectOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    status_effects_model = StatusEffectModel.from_orm_list(status_effects_orm)
    return IndexSchema(data=status_effects_model, pagination=pagination)


class GetSchema(BaseModel):
    data: StatusEffectModel


@router.get("/{status_effect_id}", response_model=GetSchema)
def get(status_effect_id: str, session=Depends(has_session)):
    status_effect_orm = (
        select(StatusEffectOrm)
        .where(StatusEffectOrm.where_slug_or_id(status_effect_id))
        .get_scalar(session)
    )
    status_effect_model = StatusEffectModel.from_orm(status_effect_orm)
    return GetSchema(data=status_effect_model)
