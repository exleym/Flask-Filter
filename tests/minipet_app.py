import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from flask_filter import FlaskFilter


db = SQLAlchemy()
filtr = FlaskFilter()


def create_app(env='test'):
    app = Flask('Mini Pet Store')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    filtr.init_app(app)
    filtr.register_model(Dog, DogSchema)
    return app


dog_toys = db.Table(
    "dog_toys",
    db.Column("dog_id", db.Integer, db.ForeignKey("dog.id")),
    db.Column("toy_id", db.Integer, db.ForeignKey("toy.id"))
)


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    dob = db.Column(db.Date)
    weight = db.Column(db.Float)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    toys = db.relationship("Toy", secondary="dog_toys", backref="dogs")

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
    created = fields.AwareDateTime()
    toys = fields.List(fields.Nested("ToySchema"))


class Toy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return f"<Toy(id={self.id}, name='{self.name}')>"


class ToySchema(Schema):
    id = fields.Integer()
    name = fields.String()
