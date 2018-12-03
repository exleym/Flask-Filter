import abc
from typing import Any


class Filter(abc.ABC):
    OP = None

    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def __repr__(self):
        return f"<{type(self).__name__}(field='{self.field}', op='{self.OP}', value={self.value})>"

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __hash__(self):
        return hash((self.field, self.OP, self.value))
