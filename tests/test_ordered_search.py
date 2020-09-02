""" Test module for validating the order_by functionality provided
as part of the search queries
"""
import unittest
from datetime import date

from flask_filter.query_filter import query_with_filters
from tests.minipet_app import create_app, filtr, Dog, DogSchema, db, Toy, ToySchema


class FlaskFilterOrderTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.db = db
        self.filtr = filtr
        with self.app.app_context():
            self.db.create_all()
            self.make_dogs()
            self.make_toys()
            self.associate_dogs_with_toys()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()
        self.app = None
        self.filtr = None
        self.db = None

    def make_dogs(self):
        doggos = [
            Dog(name="Xocomil", dob=date(1990, 12, 16), weight=100),
            Dog(name="Jasmine", dob=date(1997, 4, 20), weight=40),
            Dog(name="Quick", dob=date(2000, 5, 24), weight=90),
            Dog(name="Jinx", dob=date(2005, 12, 31), weight=55),
            Dog(name="Kaya", dob=date(2009, 3, 15), weight=50)
        ]
        self.db.session.add_all(doggos)
        self.db.session.commit()

    def make_toys(self):
        toys = [
            Toy(name="Rock"),
            Toy(name="Tennis Ball"),
            Toy(name="Knotted Rope"),
            Toy(name="Kong")
        ]
        self.db.session.add_all(toys)
        self.db.session.commit()

    def associate_dogs_with_toys(self):
        self.associate("Xocomil", "Rock")
        self.associate("Xocomil", "Tennis Ball")
        self.associate("Quick", "Tennis Ball")
        self.associate("Jinx", "Kong")

    def associate(self, dog_name, toy_name):
        dog = Dog.query.filter_by(name=dog_name).one()
        toy = Toy.query.filter_by(name=toy_name).one()
        dog.toys.append(toy)
        db.session.add(dog)
        db.session.commit()

    def test_no_filter_no_order(self):
        xfilters = []
        with self.app.app_context():
            dags = self.filtr.search(Dog, xfilters, DogSchema)
        self.assertEquals(len(dags), 5)
        self.assertListEqual([d.id for d in dags], [1, 2, 3, 4, 5])

    def test_no_filter_order_by_name(self):
        xfilters = []
        expected_order = [2, 4, 5, 3, 1]
        with self.app.app_context():
            dags = self.filtr.search(Dog, xfilters, DogSchema,
                                     order_by=Dog.name)
        self.assertEquals(len(dags), 5)
        self.assertListEqual([d.id for d in dags], expected_order)

    def test_no_filter_order_by_name_as_string(self):
        xfilters = []
        expected_order = [2, 4, 5, 3, 1]
        with self.app.app_context():
            dags = self.filtr.search(Dog, xfilters, DogSchema,
                                     order_by="name")
        self.assertEquals(len(dags), 5)
        self.assertListEqual([d.id for d in dags], expected_order)

    def test_no_filter_order_by_weight(self):
        xfilters = []
        expected_order = [2, 5, 4, 3, 1]
        with self.app.app_context():
            dags = self.filtr.search(Dog, xfilters, DogSchema,
                                     order_by=Dog.weight)
        self.assertEquals(len(dags), 5)
        self.assertListEqual([d.id for d in dags], expected_order)

    def test_no_filter_order_by_weight_as_string(self):
        xfilters = []
        expected_order = [2, 5, 4, 3, 1]
        with self.app.app_context():
            dags = self.filtr.search(Dog, xfilters, DogSchema,
                                     order_by="weight")
        self.assertEquals(len(dags), 5)
        self.assertListEqual([d.id for d in dags], expected_order)

    def test_query_with_filters_function(self):
        xfilters = []
        expected_order = [2, 5, 4, 3, 1]
        with self.app.app_context():
            dags = query_with_filters(Dog, xfilters, DogSchema,
                                     order_by=Dog.weight)
        self.assertEquals(len(dags), 5)
        self.assertListEqual([d.id for d in dags], expected_order)
