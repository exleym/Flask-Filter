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
        self.assertEqual(hash(lt), hash(("weight", "<", 10.24)))

    def test_filter_comparator_equal_for_identical_instances(self):
        json = {"field": "weight", "op": "<", "value": 10.24}
        instance_1 = self.schema.load(json)
        instance_2 = self.schema.load(json)
        self.assertEqual(instance_1, instance_2)

    def test_filter_comparator_not_equal_for_different_values(self):
        json_1 = {"field": "weight", "op": "<", "value": 10.24}
        json_2 = {"field": "weight", "op": "<", "value": 10.25}
        instance_1 = self.schema.load(json_1)
        instance_2 = self.schema.load(json_2)
        self.assertNotEqual(instance_1, instance_2)

    def test_filter_comparator_not_equal_for_different_op(self):
        json_1 = {"field": "weight", "op": "<", "value": 10.24}
        json_2 = {"field": "weight", "op": ">", "value": 10.24}
        instance_1 = self.schema.load(json_1)
        instance_2 = self.schema.load(json_2)
        self.assertNotEqual(instance_1, instance_2)

    def test_filter_comparator_not_equal_for_different_fields(self):
        json_1 = {"field": "weight", "op": "<", "value": 45}
        json_2 = {"field": "id", "op": "<", "value": 45}
        instance_1 = self.schema.load(json_1)
        instance_2 = self.schema.load(json_2)
        self.assertNotEqual(instance_1, instance_2)
