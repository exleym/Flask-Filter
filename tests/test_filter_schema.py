import unittest

from flask_filter import FilterSchema
from flask_filter.filters import *


class FilterSchemaTestClass(unittest.TestCase):

    def setUp(self):
        self.schema = FilterSchema()

    def tearDown(self):
        self.schema = None

    def test_filter_schema_init(self):
        self.assertIsInstance(self.schema, FilterSchema)
        self.assertEqual(self.schema.many, False)

    def test_filter_schema_deserializes_ltfilter(self):
        json = {"field": "age", "op": "<", "value": 3}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, LTFilter)
        self.assertEqual(filter.field, "age")
        self.assertEqual(filter.OP, "<")
        self.assertEqual(filter.value, 3)

    def test_filter_schema_deserializes_ltefilter(self):
        json = {"field": "age", "op": "<=", "value": 4}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, LTEFilter)
        self.assertEqual(filter.field, "age")
        self.assertEqual(filter.OP, "<=")
        self.assertEqual(filter.value, 4)

    def test_filter_schema_deserializes_equalsfilter(self):
        json = {"field": "age", "op": "=", "value": 2}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, EqualsFilter)
        self.assertEqual(filter.field, "age")
        self.assertEqual(filter.OP, "=")
        self.assertEqual(filter.value, 2)

    def test_filter_schema_deserializes_gtfilter(self):
        json = {"field": "age", "op": ">", "value": 1}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, GTFilter)
        self.assertEqual(filter.field, "age")
        self.assertEqual(filter.OP, ">")
        self.assertEqual(filter.value, 1)

    def test_filter_schema_deserializes_gtefilter(self):
        json = {"field": "age", "op": ">=", "value": 3}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, GTEFilter)
        self.assertEqual(filter.field, "age")
        self.assertEqual(filter.OP, ">=")
        self.assertEqual(filter.value, 3)

    def test_filter_schema_deserializes_infilter(self):
        json = {"field": "age", "op": "in", "value": [3, 4, 5]}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, InFilter)
        self.assertEqual(filter.field, "age")
        self.assertEqual(filter.OP, "in")
        self.assertEqual(filter.value, [3, 4, 5])

    def test_filter_schema_deserializes_notequalsfilter(self):
        json = {"field": "age", "op": "!=", "value": 3}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, NotEqualsFilter)
        self.assertEqual(filter.field, "age")
        self.assertEqual(filter.OP, "!=")
        self.assertEqual(filter.value, 3)

    def test_filter_schema_deserializes_likefilter(self):
        json = {"field": "name", "op": "like", "value": "charlie"}
        filter = self.schema.load(json)
        self.assertIsInstance(filter, LikeFilter)
        self.assertEqual(filter.field, "name")
        self.assertEqual(filter.OP, "like")
        self.assertEqual(filter.value, "charlie")
