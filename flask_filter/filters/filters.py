import abc

from typing import Any
from marshmallow.exceptions import ValidationError


class Filter(abc.ABC):
    OP = None

    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def __repr__(self):
        return f"<{type(self).__name__}(field='{self.field}', op='{self.OP}'" \
               f", value={self.value})>"

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __hash__(self):
        return hash((self.field, self.OP, self.value))

    @abc.abstractmethod
    def apply(self, query, class_, schema):
        raise NotImplementedError('apply is an abstract method')

    def _get_db_field(self, schema):
        """ private method to convert JSON field to SQL column

        :param schema: optional Marshmallow schema to map field -> column
        :return: string field name
        """
        if not schema:
            return self.field
        attr = schema._declared_fields.get(self.field)
        if not attr:
            raise ValidationError("'{}' is not a valid field")
        return attr.attribute or self.field


class LTFilter(Filter):
    OP = "<"

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) < self.value)


class LTEFilter(Filter):
    OP = "<="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) <= self.value)


class EqualsFilter(Filter):
    OP = "="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) == self.value)


class GTFilter(Filter):
    OP = ">"

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) > self.value)


class GTEFilter(Filter):
    OP = ">="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) >= self.value)


class InFilter(Filter):
    OP = "in"

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field).in_(self.value))


class NotEqualsFilter(Filter):
    OP = "!="

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field) != self.value)


class LikeFilter(Filter):
    OP = "like"

    def apply(self, query, class_, schema=None):
        field = self._get_db_field(schema)
        return query.filter(getattr(class_, field).like(self.value))
