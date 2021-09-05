import os

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from slugify import slugify


class BaseOrm(object):
  def as_dict_for_import(self):
    d = { c.name: getattr(self, c.name) for c in self.__table__.columns }
    d.pop('id', None)
    return d

  @classmethod
  def get_all(orm, session, options = []):
    stmt = select(orm).options(*options)
    return session.execute(stmt).scalars().all()

  @classmethod
  def get_by_slug_or_id(orm, session, slug_or_id: str, options = []):
    stmt = select(orm).where(
      orm.id == slug_or_id if slug_or_id.isdigit() else orm.slug == slug_or_id
    ).options(*options)
    return session.execute(stmt).scalars().one()


BaseOrm = declarative_base(cls=BaseOrm)


def build_session():
  return sessionmaker(create_engine(os.environ['DATABASE_URL'], echo=True, future=True))


def has_session():
  with build_session().begin() as session:
    yield session


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