import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from flask_filter import FlaskFilter


db = SQLAlchemy()
filtr = FlaskFilter()


def create_app(env='test'):
    app = Flask('Mini Pet Store')
    db.init_app(app)
    filtr.init_app(app)
    filtr.register_model(Dog, DogSchema)
    return app


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    dob = db.Column(db.Date)
    weight = db.Column(db.Float)

    @property
    def age(self):
        return int((datetime.date.today() - self.dob).days / 365.25)

    def __repr__(self):
        return f"<Dog(id={self.id}, name='{self.name}')>"


class DogSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    dateOfBirth = fields.Date(attribute='dob')
    weight = fields.Float()
