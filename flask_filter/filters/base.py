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