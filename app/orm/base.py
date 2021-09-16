from enum import Enum

from sqlalchemy.util.langhelpers import public_factory
from app.models.base import BaseModelOrm
from typing import Optional
import os

from pydantic.main import BaseModel
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import Query
from sqlalchemy.sql.selectable import Select

from slugify import slugify

class PaginationSchema(BaseModel):
  page: int
  size: int

class SortDirections(str, Enum):
  asc='asc'
  desc='desc'

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
    return self.limit(pagination.size).offset(pagination.page * pagination.size)

  def get_scalars(self, session):
    return session.execute(self).scalars().all()

  def get_scalar(self, session):
    return session.execute(self).scalars().one()

  def where_slug_or_id(self, slug_or_id: str):
    self.where(orm.id == slug_or_id if slug_or_id.isdigit() else orm.slug == slug_or_id)

select = public_factory(CustomSelect._create, ".base")

engine = create_engine(os.environ['DATABASE_URL'], echo=True, future=True)
Session = sessionmaker(engine)

class BaseOrm(object):
  def as_dict_for_import(self):
    d = { c.name: getattr(self, c.name) for c in self.__table__.columns }
    d.pop('id', None)
    return d

  @classmethod
  def where_slug_or_id(orm, slug_or_id: str):
    return orm.id == slug_or_id if slug_or_id.isdigit() else orm.slug == slug_or_id


BaseOrm = declarative_base(cls=BaseOrm)


def to_slug(to_slug_value):
  if to_slug_value:
    return slugify(to_slug_value)
  else:
    return None


def slug_default(column, target):
  to_slug_value = target[column]
  target["slug"] = to_slug(to_slug_value)


def build_slug_defaulter(column):
  def slug_defaulter(context):
      to_slug_value = context.get_current_parameters()[column]
      return to_slug(to_slug_value)

  return slug_defaulter