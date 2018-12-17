import datetime
from datetime import date
import unittest

from marshmallow.exceptions import ValidationError

from flask_filter.schemas import FilterSchema
from flask_filter.filters import *


class FilterSchemaTestClass(unittest.TestCase):

    def setUp(self):
        self.schema = FilterSchema()

    def tearDown(self):
        self.schema = None

    def test_ltfilter_accepts_floats(self):
        json = {"field": "weight", "op": "<", "value": 10.24}
        lt = self.schema.load(json)
        self.assertIsInstance(lt, LTFilter)

    def test_ltfilter_accepts_ints(self):
        json = {"field": "weight", "op": "<", "value": 10}
        lt = self.schema.load(json)
        self.assertIsInstance(lt, LTFilter)

    def test_ltfilter_accepts_dates(self):
        json = {"field": "dateOfBirth", "op": "<", "value": "2018-12-15"}
        lt = self.schema.load(json)
        self.assertIsInstance(lt, LTFilter)
        self.assertIsInstance(lt.value, datetime.date)

    def test_ltfilter_raises_validationerror_against_string(self):
        json = {"field": "name", "op": "<", "value": "Fido"}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_ltefilter_accepts_floats(self):
        json = {"field": "weight", "op": "<=", "value": 10.24}
        lte = self.schema.load(json)
        self.assertIsInstance(lte, LTEFilter)

    def test_ltefilter_accepts_ints(self):
        json = {"field": "weight", "op": "<=", "value": 10}
        lte = self.schema.load(json)
        self.assertIsInstance(lte, LTEFilter)

    def test_ltefilter_accepts_dates(self):
        json = {"field": "dateOfBirth", "op": "<=", "value": "2018-12-15"}
        lte = self.schema.load(json)
        self.assertIsInstance(lte, LTEFilter)
        self.assertIsInstance(lte.value, datetime.date)

    def test_ltefilter_raises_validationerror_against_string(self):
        json = {"field": "name", "op": "<=", "value": "Fido"}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_gtfilter_accepts_floats(self):
        json = {"field": "weight", "op": ">", "value": 10.24}
        gt = self.schema.load(json)
        self.assertIsInstance(gt, GTFilter)

    def test_gtfilter_accepts_ints(self):
        json = {"field": "weight", "op": ">", "value": 10}
        gt = self.schema.load(json)
        self.assertIsInstance(gt, GTFilter)

    def test_gtfilter_accepts_dates(self):
        json = {"field": "dateOfBirth", "op": ">", "value": "2018-12-15"}
        gt = self.schema.load(json)
        self.assertIsInstance(gt, GTFilter)
        self.assertIsInstance(gt.value, datetime.date)

    def test_gtfilter_raises_validationerror_against_string(self):
        json = {"field": "name", "op": ">", "value": "Fido"}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_gtefilter_accepts_floats(self):
        json = {"field": "weight", "op": ">=", "value": 10.24}
        gte = self.schema.load(json)
        self.assertIsInstance(gte, GTEFilter)

    def test_gtefilter_accepts_ints(self):
        json = {"field": "weight", "op": ">=", "value": 10}
        gte = self.schema.load(json)
        self.assertIsInstance(gte, GTEFilter)

    def test_gtefilter_accepts_dates(self):
        json = {"field": "dateOfBirth", "op": ">=", "value": "2018-12-15"}
        gte = self.schema.load(json)
        self.assertIsInstance(gte, GTEFilter)
        self.assertIsInstance(gte.value, datetime.date)

    def test_gtefilter_raises_validationerror_against_string(self):
        json = {"field": "name", "op": ">=", "value": "Fido"}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_equalfilter_accepts_ints(self):
        json = {"field": "weight", "op": "=", "value": 10}
        eq = self.schema.load(json)
        self.assertIsInstance(eq, EqualsFilter)

    def test_equalfilter_accepts_strings(self):
        json = {"field": "name", "op": "=", "value": "Fido"}
        eq = self.schema.load(json)
        self.assertIsInstance(eq, EqualsFilter)

    def test_equalfilter_accepts_dates(self):
        json = {"field": "name", "op": "=", "value": "2018-12-15"}
        eq = self.schema.load(json)
        self.assertIsInstance(eq, EqualsFilter)

    def test_equalsfilter_raises_validationerror_against_float(self):
        json = {"field": "weight", "op": "=", "value": 12.345}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_infilter_accepts_list_of_ints(self):
        json = {"field": "weight", "op": "in", "value": [1, 2, 3]}
        infilter = self.schema.load(json)
        self.assertIsInstance(infilter, InFilter)

    def test_infilter_accepts_list_of_strings(self):
        json = {"field": "weight", "op": "in", "value": ['A', 'B', 'C']}
        infilter = self.schema.load(json)
        self.assertIsInstance(infilter, InFilter)

    def test_infilter_accepts_list_of_dates(self):
        dates = [date(2018, 12, 15), date(2018, 12, 16)]
        json = {"field": "weight", "op": "in", "value": dates}
        infilter = self.schema.load(json)
        self.assertIsInstance(infilter, InFilter)

    def test_infilter_accepts_string_and_converts_to_list(self):
        json = {"field": "name", "op": "in", "value": "Fido"}
        infilter = self.schema.load(json)
        self.assertIsInstance(infilter, InFilter)
        self.assertEqual(infilter.value, ["Fido"])

    def test_notequalsfilter_accepts_string(self):
        json = {"field": "name", "op": "!=", "value": "Fido"}
        notequalsfilter = self.schema.load(json)
        self.assertIsInstance(notequalsfilter, NotEqualsFilter)

    def test_notequalsfilter_accepts_int(self):
        json = {"field": "age", "op": "!=", "value": 10}
        notequalsfilter = self.schema.load(json)
        self.assertIsInstance(notequalsfilter, NotEqualsFilter)

    def test_notequalsfilter_accepts_date(self):
        json = {"field": "name", "op": "!=", "value": date(2018, 12, 16)}
        notequalsfilter = self.schema.load(json)
        self.assertIsInstance(notequalsfilter, NotEqualsFilter)

    def test_notequalsfilter_fails_on_float(self):
        json = {"field": "age", "op": "!=", "value": 10.234}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_likefilter_accepts_strings(self):
        json = {"field": "name", "op": "like", "value": "Fido%"}
        likefilter = self.schema.load(json)
        self.assertIsInstance(likefilter, LikeFilter)

    def test_likefilter_fails_on_int(self):
        json = {"field": "age", "op": "like", "value": 4}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_likefilter_fails_on_float(self):
        json = {"field": "age", "op": "like", "value": 4.20}
        with self.assertRaises(ValidationError):
            self.schema.load(json)

    def test_likefilter_fails_on_date(self):
        json = {"field": "dateOfBirth", "op": "like", "value": date(2018, 12, 17)}
        with self.assertRaises(ValidationError):
            self.schema.load(json)
