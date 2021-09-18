import inspect
from enum import Enum
from typing import Dict, List, Optional, Union
from functools import reduce
from pydantic.fields import ModelField

from pydantic.main import BaseModel
from pydantic.types import conint
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.base import instance_str
from sqlalchemy.sql.selectable import Select
from sqlalchemy.util.langhelpers import public_factory
from sqlalchemy.sql import sqltypes
from sqlalchemy.dialects import postgresql

from app.orm.base import Session


class PaginationSchema(BaseModel):
    page: conint(ge=0)
    size: conint(gt=0)


class SortDirections(str, Enum):
    asc = "asc"
    desc = "desc"

filter_comparators_to_sql_function = {
    "==": "__eq__",
    "!=": "__ne__",
    ">": "__gt__",
    ">=": "__gte__",
    "<": "__lt__",
    "<=": "__lte__",
    "between": "between",
    "is_null": "is_",
    "is_not_null": "is_not",
    "@>": "contains",
    "<@": "contained_by",
    "&&": "overlap",
    "like": "like",
    "ilike": "ilike",
}

class NumericFilterComparators(str, Enum):
    eq = "=="
    ne = "!="
    gt = ">"
    gte = ">="
    lt = "<"
    lte = "<="
    between = "between"
    is_null = "is_null"
    is_not_null = "is_not_null"


class StringFilterComparators(str, Enum):
    eq = "=="
    ne = "!="
    gt = ">"
    gte = ">="
    lt = "<"
    lte = "<="
    is_null = "is_null"
    is_not_null = "is_not_null"
    like = "like"
    ilike = "ilike"


class ArrayFilterComparators(str, Enum):
    is_null = "is_null"
    is_not_null = "is_not_null"
    contains = "@>"
    contained_by = "<@"
    overlap = "&&"

def strs_to_enum(name, list: List[str]):
    list_of_tuples = [(str, str) for str in list]
    return Enum(name, list_of_tuples, type=str)

def build_filtering_schema(fields: List[InstrumentedAttribute]):
    filters_by_type = {
        "int": [],
        "str": [],
        "array": [],
    }

    for field in fields:
        type = field.type
        if isinstance(type, sqltypes.Integer) or isinstance(type, sqltypes.Numeric):
            filters_by_type["int"].append(field.name)
        elif isinstance(type, postgresql.ARRAY):
            filters_by_type["array"].append(field.name)
        else:
            filters_by_type["str"].append(field.name)

    def fields_to_enum(acc, type_fields):
        type, fields = type_fields
        filename = inspect.stack()[1].filename
        enum_name = f"{filename}{type}FilterEnum"
        acc[type] = strs_to_enum(enum_name, fields)
        return acc

    filter_type_enums = reduce(fields_to_enum, filters_by_type.items(), {})

    class ArrayFilterSchema(BaseModel):
        field: filter_type_enums['array']
        comparator: ArrayFilterComparators
        value: Union[List[str], List[int], None]

    filter_schemas = []

    if len(filter_type_enums['int']):
        class IntFilterSchema(BaseModel):
            field: filter_type_enums['int']
            comparator: NumericFilterComparators
            value: Union[int, float, None]
        filter_schemas.append(IntFilterSchema)

    if len(filter_type_enums['str']):
        class StrFilterSchema(BaseModel):
            field: filter_type_enums['str']
            comparator: StringFilterComparators
            value: Union[str, None]
        filter_schemas.append(StrFilterSchema)

    if len(filter_type_enums['array']):
        class ArrayFilterSchema(BaseModel):
            field: filter_type_enums['array']
            comparator: ArrayFilterComparators
            value: Union[List[str], List[int], None]
        filter_schemas.append(ArrayFilterSchema)

    class FiltersSchema(BaseModel):
        filters: List[Union[tuple(filter_schemas)]]

    return FiltersSchema


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

    def filter(self, orm, filter: Dict):
        field = getattr(orm, filter.field)
        comparator_func_name = filter_comparators_to_sql_function[filter.comparator]
        comparator = getattr(field, comparator_func_name)
        return self.where(comparator(filter.value))

    def filters(self, orm, filters):
        print(filters)
        if not len(filters):
            return self
        filter = filters[:1][0]
        filters = filters[1:]
        if len(filters):
            return self.filter(orm, filter).filters(orm, filters)
        else:
            return self.filter(orm, filter)

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
