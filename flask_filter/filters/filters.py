import abc
import datetime
import logging
import re

from typing import Any
from numbers import Number
from marshmallow.exceptions import ValidationError


logger = logging.getLogger(__name__)
RE_DATE = "^([0-9]{4})-([0-9]|1[0-2]|0[1-9])-([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
RE_DATETIME = "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"


def is_date(value: str) -> bool:
    return bool(re.match(RE_DATE, value))


def is_datetime(value: str) -> bool:
    return bool(re.match(RE_DATETIME, value))



class Filter(abc.ABC):
    OP = None

    def __init__(self, field: str, value: Any):
        self.nested = None
        self.set_field(field)
        self.value = self._date_or_value(value)
        self.is_valid()

    def __repr__(self):
        return f"<{type(self).__name__}(field='{self.field}', op='{self.OP}'" \
               f", value={self.value})>"

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.field, self.OP, self.value))

    def set_field(self, field):
        f = field.split(".")
        self.field = f[0]
        if len(f) == 2:
            self.nested = f[1]
        elif len(f) > 2:
            logger.warning(
                f"you supplied nested fields {f}. Only one level of nesting "
                f"is currently supported. ignoring fields {f[2:]}."
            )

    @abc.abstractmethod
    def apply(self, query, class_, schema):
        raise NotImplementedError('apply is an abstract method')

    @abc.abstractmethod
    def is_valid(self):
        raise NotImplementedError('is_valid is an abstract method')

    def _get_db_field(self, schema):
        """ private method to convert JSON field to SQL column

        :param schema: optional Marshmallow schema to map field -> column
        :return: string field name
        """
        if not schema:
            return self.field
        attr = schema._declared_fields.get(self.field)
        if not attr:
            raise ValidationError(f"'{attr}' is not a valid field")
        return attr.attribute or self.field

    def _date_or_value(self, value):
        if not isinstance(value, str):
            return value
        elif is_date(value):
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        elif is_datetime(value):
            return self._parse_datetime(value)
        return value

    def _parse_datetime(self, value: str):
        dt = value.replace("Z", "+00:00")
        return datetime.datetime.fromisoformat(dt)


class RelativeComparator(Filter):

    def is_valid(self):
        try:
            allowed = (Number, datetime.date, datetime.datetime)
            assert isinstance(self.value, allowed)
        except AssertionError:
            raise ValidationError(f"{self} requires an ordinal value")


class LTFilter(RelativeComparator):
    OP = "<"

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) < self.value)


class LTEFilter(RelativeComparator):
    OP = "<="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) <= self.value)


class GTFilter(RelativeComparator):
    OP = ">"

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) > self.value)


class GTEFilter(RelativeComparator):
    OP = ">="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) >= self.value)


class EqualsFilter(Filter):
    OP = "="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) == self.value)

    def is_valid(self):
        allowed = (str, int, datetime.date, None.__class__)
        try:
            assert isinstance(self.value, allowed)
        except AssertionError:
            raise ValidationError(f"{self} requires a string, int, date or null value")


class InFilter(Filter):
    OP = "in"

    def __init__(self, field: str, value: Any):
        if isinstance(value, str):
            value = [value]
        super().__init__(field, value)

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field).in_(list(self.value)))

    def is_valid(self):
        try:
            _ = (e for e in self.value)
        except TypeError:
            raise ValidationError(f"{self} must be an iterable")


class NotEqualsFilter(Filter):
    OP = "!="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) != self.value)

    def is_valid(self):
        allowed = (str, int, datetime.date, None.__class__)
        try:
            assert isinstance(self.value, allowed)
        except AssertionError:
            raise ValidationError(f"{self} requires a string, int, date or null value")


class LikeFilter(Filter):
    OP = "like"

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field).like(self.value))

    def is_valid(self):
        try:
            assert isinstance(self.value, str)
        except AssertionError:
            raise ValidationError(f"{self} requires a string with a wildcard")


class ContainsFilter(Filter):
    OP = "contains"

    def apply(self, query, class_, schema=None):
        subfield = self.nested or "id"
        q = {subfield: self.value}
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field).any(**q))

    def is_valid(self):
        pass
