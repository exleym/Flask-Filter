import logging
import marshmallow as ma
from marshmallow.exceptions import ValidationError
from flask_filter.filters import FILTERS


__FILTER_MAP = {c.OP: c for c in FILTERS}
__VALID_OPERATORS = {x.OP for x in FILTERS}
_mm2 = ma.__version_info__[0] == 2
logger = logging.getLogger(__name__)


def _get_filter_class(operator):
    return __FILTER_MAP.get(operator)


def vali1date_operator(value):
    if value not in __VALID_OPERATORS:
        message = {'op': [f"operator {value} is not supported"]}
        raise ValidationError(message)


class FilterSchema(ma.Schema):
    field = ma.fields.String(required=True, allow_none=False)
    op = ma.fields.String(required=True, attribute="OP", validate=vali1date_operator)
    value = ma.fields.Field(required=True, allow_none=False)

    @ma.post_load
    def make_object(self, json, *args, **kwargs):
        op = json.get("OP")
        field = json.get("field")
        value = json.get("value")
        Class = _get_filter_class(op)
        return Class(field=field, value=value)


_schema = FilterSchema()


def deserialize_filters(data, *args, **kwargs):
    """ centralizes marshmallow v2/v3 api change handling to one place.
    in future version of this we can remove all mm2 support and this
    function will be a one-liner.
    """
    data = _schema.load(data, *args, **kwargs)
    if _mm2:
        logger.warning(f"Marshmallow v2 is deprecated and will not be "
                       f"supported in future versions of FlaskFilter. "
                       f"Please upgrade to Marshmallow 3+")
        data = data.data
    return data
