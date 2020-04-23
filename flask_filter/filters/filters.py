import abc
import datetime
import logging
import re

from typing import Any
from numbers import Number
from marshmallow.exceptions import ValidationError


logger = logging.getLogger(__name__)
RE_DATE = "^([0-9]{4})-([0-9]|1[0-2]|0[1-9])-([1-9]|0[1-9]|1[0-9]|2[1-9]|3[0-1])$"


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
        if re.match(RE_DATE, value):
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        return value


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
        allowed = (str, int, datetime.date)
        try:
            assert isinstance(self.value, allowed)
        except AssertionError:
            raise ValidationError(f"{self} requires a string or int value")


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
        try:
            assert type(self.value) in (str, int, datetime.date)
        except AssertionError:
            raise ValidationError(f"{self} requires a string or int value")


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
