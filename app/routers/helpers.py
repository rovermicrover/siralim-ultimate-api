import inspect
from enum import Enum
from typing import Dict, Optional
from pydantic.main import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.selectable import Select
from sqlalchemy.util.langhelpers import public_factory

from app.orm.base import Session


class PaginationSchema(BaseModel):
    page: int
    size: int


class SortDirections(str, Enum):
    asc = "asc"
    desc = "desc"


class SortingSchema(object):
    def __init__(self, by: InstrumentedAttribute, direction: SortDirections):
        self.by = by
        self.direction = direction


class CustomSelect(Select):
    def sorting(self, sorting: SortingSchema):
        order_by = sorting.by
        if sorting.direction == SortDirections.desc:
            order_by = order_by.desc()
        return self.order_by(order_by)

    def pagination(self, pagination: PaginationSchema):
        return self.limit(pagination.size).offset(
            pagination.page * pagination.size
        )

    def get_scalars(self, session):
        return session.execute(self).scalars().all()

    def get_scalar(self, session):
        return session.execute(self).scalars().one()


select = public_factory(CustomSelect._create, ".base")


def has_session():
    with Session.begin() as session:
        yield session


def has_pagination(default_size: Optional[int] = 25):
    def _has_pagination(
        page: Optional[int] = 0, size: Optional[int] = default_size
    ) -> PaginationSchema:
        return PaginationSchema(page=page, size=size)

    return _has_pagination


def has_sorting(
    sortables: Dict[str, InstrumentedAttribute], default_sort_by: str
):
    has_sorting_enum_tuples = [(key, key) for key in sortables.keys()]
    filename = inspect.stack()[1].filename
    has_sorting_enum = Enum(
        f"{filename}HasSortingEnum", has_sorting_enum_tuples, type=str
    )
    default_sort_by_enum = has_sorting_enum[default_sort_by]

    def _has_sorting(
        sort_by: Optional[has_sorting_enum] = default_sort_by_enum,
        sort_direction: Optional[SortDirections] = SortDirections.asc,
    ) -> SortingSchema:
        by = sortables[sort_by]
        return SortingSchema(by=by, direction=sort_direction)

    return _has_sorting
