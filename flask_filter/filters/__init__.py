from flask_filter.filters.base_filter import Filter


class LTFilter(Filter):
    OP = "<"


class LTEFilter(Filter):
    OP = "<="


class EqualsFilter(Filter):
    OP = "="


class GTFilter(Filter):
    OP = ">"


class GTEFilter(Filter):
    OP = ">="


class InFilter(Filter):
    OP = "in"


class NotEqualsFilter(Filter):
    OP = "ne"


FILTERS = [
    LTFilter,
    LTEFilter,
    EqualsFilter,
    GTFilter,
    GTEFilter,
    InFilter,
    NotEqualsFilter
]