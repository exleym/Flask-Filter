import unittest

from flask_filter import FilterSchema


class FilterSchemaTestClass(unittest.TestCase):

    def setUp(self):
        self.schema = FilterSchema()

    def tearDown(self):
        self.schema = None

    def test_filter_schema_init(self):
        self.assertIsInstance(self.schema, FilterSchema)
        self.assertEqual(self.schema.many, False)
        self.assertEqual(self.schema.strict, False)
