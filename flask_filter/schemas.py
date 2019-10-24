from marshmallow import Schema, fields, post_load
from marshmallow.exceptions import ValidationError
from flask_filter.filters import FILTERS


__FILTER_MAP = {c.OP: c for c in FILTERS}
__VALID_OPERATORS = {x.OP for x in FILTERS}


def _get_filter_class(operator):
    return __FILTER_MAP.get(operator)


def vali1date_operator(value):
    if value not in __VALID_OPERATORS:
        message = {'op': [f"operator {value} is not supported"]}
        raise ValidationError(message)


class FilterSchema(Schema):
    field = fields.String(required=True, allow_none=False)
    op = fields.String(required=True, attribute="OP", validate=vali1date_operator)
    value = fields.Field(required=True, allow_none=False)

    @post_load
    def make_object(self, json, *args, **kwargs):
        op = json.get("OP")
        field = json.get("field")
        value = json.get("value")
        Class = _get_filter_class(op)
        return Class(field=field, value=value)
