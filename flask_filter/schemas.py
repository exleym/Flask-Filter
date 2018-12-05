from marshmallow import Schema, fields, post_load
from marshmallow.exceptions import ValidationError
from flask_filter.filters import *


def get_filter_class(operator):
    filter_dict = {c.OP: c for c in FILTERS}
    return filter_dict.get(operator)


def vali1date_operator(value):
    if value not in [x.OP for x in FILTERS]:
        message = {'op': [f"operator {value} is not supported"]}
        raise ValidationError(message)


class FilterSchema(Schema):
    field = fields.String(required=True, allow_none=False)
    op = fields.String(required=True, attribute="OP", validate=vali1date_operator)
    value = fields.Field(required=True, allow_none=False)

    @post_load
    def make_object(self, json):
        op = json.get("OP")
        field = json.get("field")
        value = json.get("value")
        Class = get_filter_class(op)
        return Class(field=field, value=value)