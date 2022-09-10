import datetime as dt
import pytest
from tests.minipet_app import create_app, Dog, DogSchema, db


@pytest.fixture
def minipet_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()
    app = None


@pytest.fixture
def minipet_app_datafied(minipet_app):
    with minipet_app.app_context():
        make_dogs()
    yield minipet_app



def make_dogs():
    doggos = [
        Dog(name="Xocomil", dob=dt.date(1990, 12, 16), weight=100),
        Dog(name="Jasmine", dob=dt.date(1997, 4, 20), weight=40),
        Dog(name="Quick", dob=dt.date(2000, 5, 24), weight=90),
        Dog(name="Jinx", dob=dt.date(2005, 12, 31), weight=55),
        Dog(name="Kaya", dob=None, weight=50),
        Dog(name="Bozeman", dob=dt.date(2021, 12, 22), weight=45)
    ]
    db.session.add_all(doggos)
    db.session.commit()
