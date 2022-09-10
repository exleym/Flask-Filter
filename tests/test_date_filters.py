import datetime as dt
import pytest
import pytz
from flask_filter.filters.filters import is_date, is_datetime
from flask_filter.query_filter import query_with_filters
from flask_filter.schemas import FilterSchema
from tests.minipet_app import Dog, DogSchema


@pytest.mark.parametrize(
    "op,value,expected",
    [
        (">", "2022-04-20", dt.date(2022, 4, 20)),
        ("<", "2022-09-10", dt.date(2022, 9, 10)),
        ("=", "2022-10-24", dt.date(2022, 10, 24)),
    ]
)
def test_filters_deserialize_isodate(op, value, expected):
    schema = FilterSchema()
    data = {"field": "foo", "op": op, "value": value}
    ftr = schema.load(data)
    assert ftr.value == expected


@pytest.mark.parametrize(
    "isodate",
    [
        "2022-01-01", "2022-01-09", "2022-01-10", "2022-01-19", "2022-01-20", "2022-01-29", "2022-01-30", "2022-01-31",
        "2022-02-01", "2022-02-09", "2022-02-10", "2022-02-11", "2022-02-19", "2022-02-20", "2022-02-28",
        "2022-09-01", "2022-09-09", "2022-09-10", "2022-09-19", "2022-09-20", "2022-09-21", "2022-09-29", "2022-09-30",
        "2022-10-01", "2022-10-09", "2022-10-10", "2022-10-19", "2022-10-20", "2022-10-29", "2022-10-30", "2022-10-31",
        "2022-11-01", "2022-11-09", "2022-11-10", "2022-11-19", "2022-11-20", "2022-11-21", "2022-11-29", "2022-11-30",
        "2022-12-01", "2022-12-09", "2022-12-10", "2022-12-19", "2022-12-20", "2022-12-21", "2022-12-29", "2022-12-30",
        "2022-12-31"
    ]
)
def test_date_regex(isodate):
    assert is_date(isodate)


@pytest.mark.parametrize(
    "isodatetime",
    ["2022-04-01T11:34:34-00:00", "2022-04-20T16:20:00Z"]
)
def test_datetime_regex(isodatetime):
    assert is_datetime(isodatetime)


@pytest.mark.parametrize(
    "op,value,expected",
    [
        (">", "2022-04-20T16:20:00+00:00", dt.datetime(2022, 4, 20, 16, 20, 0, tzinfo=dt.timezone.utc)),
        (">", "2022-04-20T16:20:00Z", dt.datetime(2022, 4, 20, 16, 20, 0, tzinfo=dt.timezone.utc)),
        (">", "2022-04-20T16:20:00-04:00", dt.datetime(2022, 4, 20, 16, 20, 0, tzinfo=dt.timezone(dt.timedelta(days=-1, seconds=72000)))),
    ]
)
def test_filters_deserialize_isodate(op, value, expected):
    schema = FilterSchema()
    data = {"field": "foo", "op": op, "value": value}
    print(f"attempting to load {data} with FilterSchema()")
    ftr = schema.load(data)
    assert ftr.value == expected



def test_datetime_lt_search(minipet_app_datafied):
    """dogs are inserted into the database with a default created timestamp of UTCNOW

    for this test, we expect all dogs in default database (which are created before
    the test is executed) to have a created timestamp before the test. Thus, 100%
    of dogs in database should match this filter
    """
    now = dt.datetime.utcnow()
    xfilters = [{"field": "created", "op": "<", "value": now.isoformat()}]
    with minipet_app_datafied.app_context():
        already_created = query_with_filters(Dog, xfilters, DogSchema)
    assert len(already_created) == 6


def test_datetime_gt_search(minipet_app_datafied):
    """dogs are inserted into the database with a default created timestamp of UTCNOW

    for this test, we expect all dogs in default database (which are created before
    the test is executed) to have a created timestamp before the test. Thus, no
    dogs in database should match this filter
    """
    now = dt.datetime.utcnow()
    xfilters = [{"field": "created", "op": ">", "value": now.isoformat()}]
    with minipet_app_datafied.app_context():
        not_yet_created = query_with_filters(Dog, xfilters, DogSchema)
    assert len(not_yet_created) == 0
