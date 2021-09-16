from enum import Enum
from typing import Dict, Optional
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.orm.base import Session
from app.orm.base import PaginationSchema, SortDirections, SortingSchema

def has_session():
  with Session.begin() as session:
    yield session

def has_pagination(default_size: Optional[int] = 25):
  def _has_pagination(page: Optional[int] = 0, size: Optional[int] = default_size) -> PaginationSchema:
    return PaginationSchema(page=page, size=size)
  return _has_pagination

def has_sorting(sortables: Dict[str, InstrumentedAttribute], default_sort_by: str):
  has_sorting_enum_tuples = [(key, key) for key in sortables.keys()]
  has_sorting_enum = Enum('HasSortingEnum', has_sorting_enum_tuples, type=str)
  default_sort_by_enum = has_sorting_enum[default_sort_by]

  def _has_sorting(
    sort_by: Optional[has_sorting_enum] = default_sort_by_enum, 
    sort_direction: Optional[SortDirections] = SortDirections.asc
  ) -> SortingSchema:
    by = sortables[sort_by]
    return SortingSchema(by=by, direction=sort_direction)
  return _has_sorting