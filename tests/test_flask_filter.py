import unittest
from datetime import date

from flask_filter import FlaskFilter
from tests.minipet_app import create_app, filtr, Dog, DogSchema, db, Toy, ToySchema


class FlaskFilterTestClass(unittest.TestCase):

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
            Dog(name="Kaya", dob=None, weight=50)
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

    def test_doggos_exist(self):
        with self.app.app_context():
            doggos = Dog.query.all()
        self.assertEqual(len(doggos), 5)

    def test_name_equalsfilter(self):
        xfilters = [{"field": "name", "op": "=", "value": "Xocomil"}]
        with self.app.app_context():
            xoco = self.filtr.search(Dog, xfilters, DogSchema)
        self.assertEqual(len(xoco), 1)
        self.assertEqual(xoco[0].name, "Xocomil")

    def test_name_likefilter(self):
        filters = [{"field": "name", "op": "like", "value": "J%"}]
        with self.app.app_context():
            j_dogs = self.filtr.search(Dog, filters, DogSchema)
        self.assertEqual(len(j_dogs), 2)
        self.assertEqual(j_dogs[0].name, "Jasmine")
        self.assertEqual(j_dogs[1].name, "Jinx")

    def test_name_notequalsfilter(self):
        xfilters = [{"field": "name", "op": "!=", "value": "Xocomil"}]
        with self.app.app_context():
            not_xoco = self.filtr.search(Dog, xfilters, DogSchema)
        self.assertEqual(len(not_xoco), 4)

    def test_name_infilter(self):
        f = [{"field": "name", "op": "in", "value": ["Jinx", "Kaya"]}]
        with self.app.app_context():
            jinx_and_kaya = self.filtr.search(Dog, f, DogSchema)
        self.assertEqual(len(jinx_and_kaya), 2)

    def test_dob_filter(self):
        min_date = date(2002, 1, 1).isoformat()
        f = [{"field": "dateOfBirth", "op": "<", "value": min_date}]
        with self.app.app_context():
            old_dogs = self.filtr.search(Dog, f, DogSchema)
        self.assertEqual(len(old_dogs), 3)

    def test_weight_ltfilter(self):
        f = [{"field": "weight", "op": "<", "value": 50}]
        with self.app.app_context():
            skinny_dogs = self.filtr.search(Dog, f, DogSchema)
        self.assertEqual(len(skinny_dogs), 1)

    def test_weight_ltefilter(self):
        f = [{"field": "weight", "op": "<=", "value": 50}]
        with self.app.app_context():
            skinnyish_dogs = self.filtr.search(Dog, f, DogSchema)
        self.assertEqual(len(skinnyish_dogs), 2)

    def test_weight_gtfilter(self):
        f = [{"field": "weight", "op": ">", "value": 90}]
        with self.app.app_context():
            fat_dogs = self.filtr.search(Dog, f, DogSchema)
        self.assertEqual(len(fat_dogs), 1)

    def test_weight_gtefilter(self):
        f = [{"field": "weight", "op": ">=", "value": 90}]
        with self.app.app_context():
            fatish_dogs = self.filtr.search(Dog, f, DogSchema)
        self.assertEqual(len(fatish_dogs), 2)

    def test_registered_schema_against_dob(self):
        min_date = date(2002, 1, 1).isoformat()
        f = [{"field": "dateOfBirth", "op": "<", "value": min_date}]
        with self.app.app_context():
            old_dogs = self.filtr.search(Dog, f)
        self.assertEqual(len(old_dogs), 3)

    def test_registered_schema_against_weight(self):
        f = [{"field": "weight", "op": "<=", "value": 50}]
        with self.app.app_context():
            skinnyish_dogs = self.filtr.search(Dog, f)
        self.assertEqual(len(skinnyish_dogs), 2)

    def test_flaskfilter_direct_init(self):
        filtr = FlaskFilter(self.app)
        f = [{"field": "weight", "op": "<=", "value": 50}]
        with self.app.app_context():
            skinnyish_dogs = filtr.search(Dog, f, DogSchema)
        self.assertEqual(len(skinnyish_dogs), 2)

    def test_flaskfilter_search_limit(self):
        f = []
        with self.app.app_context():
            all_dogs = self.filtr.search(Dog, f)
            three_dogs = self.filtr.search(Dog, f, limit=3)
        self.assertEqual(len(all_dogs), 5)
        self.assertEqual(len(three_dogs), 3)

    def test_flaskfilter_contains(self):
        f = [{"field": "toys.id", "op": "contains", "value": 2}]
        with self.app.app_context():
            ball_dogs = self.filtr.search(Dog, f)
            self.assertEqual(len(ball_dogs), 2)
