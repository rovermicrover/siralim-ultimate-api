import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from slugify import slugify


engine = create_engine(os.environ["DATABASE_URL"], future=True)
Session = sessionmaker(engine)


class BaseOrm(object):
    def as_dict_for_import(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d.pop("id", None)
        return d

    @classmethod
    def where_slug_or_id(orm, slug_or_id: str):
        return (
            orm.id == slug_or_id
            if slug_or_id.isdigit()
            else orm.slug == slug_or_id
        )


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
