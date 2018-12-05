from .base import Filter


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
        return query.filter(getattr(class_,field).like(self.value))