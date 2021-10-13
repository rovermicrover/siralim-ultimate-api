from enum import Enum
from typing import Dict, List, Optional, Union
from functools import reduce
from uuid import uuid4
from pydantic import fields

from pydantic.main import BaseModel
from pydantic.types import conint
from sqlalchemy import or_
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.util import _ORMJoin
from sqlalchemy.sql.selectable import Select
from sqlalchemy.util.langhelpers import public_factory
from sqlalchemy.sql import sqltypes
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import ColumnAssociationProxyInstance

from app import orm as OrmMap
from app.orm.base import Session, FullText


class PaginationRequestSchema(BaseModel):
    page: conint(ge=0) = 0
    size: conint(gt=0) = 25


class PaginationResponseSchema(BaseModel):
    page: conint(ge=0)
    size: conint(gt=0)
    count: conint(ge=0)

    @classmethod
    def from_request(cls, pagination: PaginationRequestSchema, count: int):
        return cls(page=pagination.page, size=pagination.size, count=count)


class SortDirections(str, Enum):
    asc = "asc"
    desc = "desc"


filter_comparators_to_sql_function = {
    "==": "__eq__",
    "!=": "__ne__",
    ">": "__gt__",
    ">=": "__ge__",
    "<": "__lt__",
    "<=": "__le__",
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


class BoolFilterComparators(str, Enum):
    eq = "=="
    ne = "!="


class StringFilterComparators(str, Enum):
    eq = "=="
    ne = "!="
    like = "like"
    ilike = "ilike"


class ArrayFilterComparators(str, Enum):
    overlap = "&&"
    contains = "@>"
    contained_by = "<@"
    eq = "=="
    ne = "!="


class NullFilterComparators(str, Enum):
    is_null = "is_null"
    is_not_null = "is_not_null"


def strs_to_enum(name, list: List[str]):
    list_of_tuples = [(str, str) for str in list]
    return Enum(name, list_of_tuples, type=str)


def build_filtering_schema(
    name: str,
    fields: List[Union[InstrumentedAttribute, ColumnAssociationProxyInstance]],
):
    filters_by_type = {
        "int": [],
        "str": [],
        "bool": [],
        "array_str": [],
        "array_int": [],
        "all": [],
    }

    for field in fields:
        filters_by_type["all"].append(get_field_name(field))

        if isinstance(field, ColumnAssociationProxyInstance):
            type = field.attr[1].type
        else:
            type = field.type

        if isinstance(type, sqltypes.Integer) or isinstance(
            type, sqltypes.Numeric
        ):
            filters_by_type["int"].append(get_field_name(field))
        elif isinstance(type, sqltypes.Boolean):
            filters_by_type["bool"].append(get_field_name(field))
        elif isinstance(type, postgresql.ARRAY):
            if isinstance(type.item_type, sqltypes.Integer) or isinstance(
                type.item_type, sqltypes.Numeric
            ):
                filters_by_type["array_int"].append(get_field_name(field))
            else:
                filters_by_type["array_str"].append(get_field_name(field))
        else:
            filters_by_type["str"].append(get_field_name(field))

    def fields_to_enum(acc, type_fields):
        type, fields = type_fields
        enum_name = f"{name}{type.title().replace('_','')}FilterEnum"
        acc[type] = strs_to_enum(enum_name, fields)
        return acc

    filter_type_enums = reduce(fields_to_enum, filters_by_type.items(), {})

    filter_schemas = []

    if len(filter_type_enums["int"]):

        class IntFilterSchema(BaseModel):
            field: filter_type_enums["int"]
            comparator: NumericFilterComparators
            value: Union[int, float]

        IntFilterSchema.__name__ = f"{name}IntFilterSchema"

        filter_schemas.append(IntFilterSchema)

    if len(filter_type_enums["bool"]):

        class BoolFilterSchema(BaseModel):
            field: filter_type_enums["bool"]
            comparator: BoolFilterComparators
            value: Union[bool]

        BoolFilterSchema.__name__ = f"{name}BoolFilterSchema"

        filter_schemas.append(BoolFilterSchema)

    if len(filter_type_enums["str"]):

        class StrFilterSchema(BaseModel):
            field: filter_type_enums["str"]
            comparator: StringFilterComparators
            value: Union[str]

        StrFilterSchema.__name__ = f"{name}StrFilterSchema"

        filter_schemas.append(StrFilterSchema)

    if len(filter_type_enums["array_str"]):

        class ArrayStrFilterSchema(BaseModel):
            field: filter_type_enums["array_str"]
            comparator: ArrayFilterComparators
            value: Union[List[str], List[int], None]

        ArrayStrFilterSchema.__name__ = f"{name}ArrayStrFilterSchema"

        filter_schemas.append(ArrayStrFilterSchema)

    if len(filter_type_enums["array_int"]):

        class ArrayIntFilterSchema(BaseModel):
            field: filter_type_enums["array_int"]
            comparator: ArrayFilterComparators
            value: Union[List[str], List[int], None]

        ArrayIntFilterSchema.__name__ = f"{name}ArrayIntFilterSchema"

        filter_schemas.append(ArrayIntFilterSchema)

    class NullFilterSchema(BaseModel):
        field: filter_type_enums["all"]
        comparator: NullFilterComparators
        value: None

    NullFilterSchema.__name__ = f"{name}NullFilterSchema"

    filter_schemas.append(NullFilterSchema)

    class FiltersSchema(BaseModel):
        filters: List[Union[tuple(filter_schemas)]]

    FiltersSchema.__name__ = f"{name}FiltersSchema"

    return FiltersSchema


def get_field_name(
    field: Union[
        InstrumentedAttribute, ColumnAssociationProxyInstance, FullText
    ]
):
    if isinstance(field, ColumnAssociationProxyInstance):
        local, remote = field.attr
        return "_".join([local.key, remote.key])
    else:
        return field.key


def build_sorting_schema(
    name: str,
    fields: List[Union[InstrumentedAttribute, ColumnAssociationProxyInstance]],
    default_sort_by="id",
):
    enum_name = f"{name}SortingEnum"

    field_names = map(get_field_name, fields)
    sort_field_enum = strs_to_enum(enum_name, field_names)

    class SortingRequestSchema(BaseModel):
        by: sort_field_enum = default_sort_by
        direction: SortDirections = SortDirections.asc

    SortingRequestSchema.__name__ = f"{name}SortingRequestSchema"

    class SortingResponseSchema(BaseModel):
        by: sort_field_enum
        direction: SortDirections

        class Config:
            orm_mode = True

    SortingResponseSchema.__name__ = f"{name}SortingResponseSchema"

    return (SortingRequestSchema, SortingResponseSchema)


def get_comparitor(filter, field):
    comparator_func_name = filter_comparators_to_sql_function[
        filter.comparator
    ]
    if isinstance(field, ColumnAssociationProxyInstance):
        return getattr(field.attr[1], comparator_func_name)
    else:
        return getattr(field, comparator_func_name)


class CustomSelect(Select):
    def get_orm(self):
        final_from = self.get_final_froms()[0]
        while isinstance(final_from, _ORMJoin):
            final_from = final_from.left
        return getattr(OrmMap, final_from.name)

    def sorting(self, sorting):
        orm = self.get_orm()
        order_by = getattr(orm, sorting.by)
        if isinstance(order_by, FullText):
            order_by = getattr(orm, order_by.columns[0])
        if isinstance(order_by, ColumnAssociationProxyInstance):
            order_by = order_by.remote_attr
        if sorting.direction == SortDirections.desc:
            order_by = order_by.desc()
        return self.order_by(order_by, orm.name)

    def pagination(self, pagination: PaginationRequestSchema):
        return self.limit(pagination.size).offset(
            pagination.page * pagination.size
        )

    def filter(self, filter: Dict):
        orm = self.get_orm()
        field = getattr(orm, filter.field)
        if isinstance(field, FullText):
            fields = [getattr(orm, c) for c in field.columns]
            return self.where(
                or_(*[get_comparitor(filter, f)(filter.value) for f in fields])
            )
        else:
            return self.where(get_comparitor(filter, field)(filter.value))

    def filters(self, filters):
        if not len(filters):
            return self
        filter = filters[:1][0]
        filters = filters[1:]
        if len(filters):
            return self.filter(filter).filters(filters)
        else:
            return self.filter(filter)

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
    ) -> PaginationRequestSchema:
        return PaginationRequestSchema(page=page, size=size)

    return _has_pagination


def has_sorting(sorting_schema: BaseModel):
    def _has_sorting(
        sort_by: Optional[
            sorting_schema.__fields__["by"].type_
        ] = sorting_schema.__fields__["by"].default,
        sort_direction: Optional[SortDirections] = SortDirections.asc,
    ) -> sorting_schema:
        return sorting_schema(by=sort_by, direction=sort_direction)

    return _has_sorting
