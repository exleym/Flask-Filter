# Flask-Filter
Filtering Extension for Flask / SQLAlchemy

[![Build Status](https://travis-ci.org/exleym/Flask-Filter.svg?branch=master)](https://travis-ci.org/exleym/Flask-Filter)

# Introduction
Flask-Filter is a simple [Flask](http://flask.pocoo.org/) extension for
standardizing search endpoints for a REST API. It is designed to
integrate with the [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
extension and [Marshmallow](https://marshmallow.readthedocs.io/en/3.0/),
a popular serialization library.

# Default Filters
Out-of-the box, `Flask-Filter` supports filters as JSON objects with
the following structure:

```json
{"field": "field_name", "op": "operator", "value": "some_value"}
```

The built-in filters support the following operators:

| symbol   | operator                     | python filter class   |
|----------|------------------------------|-----------------------|
| <        | less-than                    | `LTFilter`            |
| <=       | less-than or equal to        | `LTEFilter`           |
| =        | equal to                     | `EqualsFilter`        |
| >        | greater-than                 | `GTFilter`            |
| >=       | greater-than or equal to     | `GTEFilter`           |
| in       | in                           | `InFilter`            |
| !=       | not equal to                 | `NotEqualsFilter`     |
| like     | like                         | `LikeFilter`          |

# Examples
This section demonstrates simplified use-cases for Flask-Filter. For
a complete example app (a Pet Store API), see the `/example` folder.

Note: examples in this readme define simple `/search` endpoints that
assume a working Flask app has already been initialized, and other
required classes have been defined in a `pet_store` directory. To see
a full implementation, go to `/examples/pet_store`

### Example 1: Manually implementing filters in a flask view
Using the `FilterSchema` class directly, you can deserialize an
array of JSON filters into a list of `flask_filter.Filter` objects
and directly apply the filters using `Filter.apply` to craft a
SQLAlchemy query with a complex set of filters.

```python
filter_schema = FilterSchema()
pet_schema = PetSchema()

@app.route('/api/v1/pets/search', methods=['POST'])
def pet_search():
    filters = filter_schema.load(request.json.get("filters"), many=True)
    query = Pet.query
    for f in filters:
        query = f.apply(query, Pet, PetSchema)
    return jsonify(pet_schema.dump(query.all())), 200
```

### Example 2: Automatically filtering using the `query_with_filters` function

```python
from flask_filter import query_with_filters
pet_schema = PetSchema()

@app.route('/api/v1/pets/search', methods=['POST']
def pet_search():
    pets = query_with_filters(Pet, request.json.get("filters"), PetSchema)
    return jsonify(pet_schema.dump(pets)), 200
```