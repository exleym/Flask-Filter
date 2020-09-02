from flask import Flask
from flask_sqlalchemy import Model
from marshmallow import Schema
from typing import Union

from flask_filter.schemas import FilterSchema



class FlaskFilter(object):
    __SCHEMA_MAP = {}

    def __init__(self, app: Flask = None):
        self.app = app
        self.schema = FilterSchema()
        if self.app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Callback for initializing application """
        self.app = app

    def register_model(self, DbModel, ModelSchema):
        self.__SCHEMA_MAP[DbModel] = ModelSchema

    def search(self, DbModel: Model, filters: list,
               ModelSchema: Union[Schema, None] = None,
               limit: int = None, order_by=None):
        filters = self.schema.load(filters, many=True)
        schema = ModelSchema or self._lookup_schema(DbModel)
        query = DbModel.query
        for f in filters:
            query = f.apply(query, DbModel, schema)
        if order_by:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit)
        return query.all()

    def _lookup_schema(self, DbModel):
        model = self.__SCHEMA_MAP.get(DbModel)
        if not model:
            raise TypeError('You must either map a schema to Model: {} using `register_model`'
                            'or pass a schema to the `ModelSchema` parameter'
                            'when calling `search`'.format(DbModel))
        return model
