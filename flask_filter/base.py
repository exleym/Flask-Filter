from flask import Flask
from flask_sqlalchemy import Model
from marshmallow import Schema
from typing import Union

from flask_filter.schemas import FilterSchema


class FlaskFilter(object):

    def __init__(self, app: Flask = None):
        self.app = app
        self.schema = FilterSchema()
        if self.app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Callback for initializing application """
        app.extensions['filter'] = _FlaskFilterState(self)
        self.app = app

    def register_model(self, DbModel, ModelSchema):
        print("\n" + "="*72)
        print(self.app.extensions)
        print(type(self.app.extensions))
        print("=" * 72 + "\n\n")
        self.app.extensions['filter'].update_state(DbModel, ModelSchema)

    def search(self, DbModel: Model, filters: list,
               ModelSchema: Union[Schema, None] = None,
               limit: int = None):
        filters = self.schema.load(filters, many=True)
        schema = ModelSchema or self._lookup_schema(DbModel)
        query = DbModel.query
        for f in filters:
            query = f.apply(query, DbModel, schema)
        if limit:
            query.limit(limit)
        return query.all()

    def _lookup_schema(self, DbModel):
        model = self.app.extensions["filter"].get_schema(DbModel)
        if not model:
            raise TypeError('You must either map a schema to Model: {} using `register_model`'
                            'or pass a schema to the `ModelSchema` parameter'
                            'when calling `search`'.format(DbModel))
        return model


class _FlaskFilterState(object):
    """Remembers configuration for the (filter, app) tuple """

    def __init__(self, filter: FlaskFilter):
        self.filter = filter
        self.schema_map = dict()

    def update_state(self, DbModel: Model, ModelSchema: Schema):
        self.schema_map[DbModel] = ModelSchema

    def get_schema(self, DbModel: Model):
        return self.schema_map.get(DbModel, None)
