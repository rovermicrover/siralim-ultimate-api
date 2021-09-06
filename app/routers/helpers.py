from typing import Optional

from app.pg import build_session
from app.orm.base import PaginationSchema


def has_session():
  with build_session().begin() as session:
    yield session

def has_pagination(default_size: Optional[int] = 25):
  def _has_pagination(page: Optional[int] = 0, size: Optional[int] = default_size) -> PaginationSchema:
    return PaginationSchema(page=page, size=size)
  return _has_pagination