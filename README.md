# Flask-Filter
Filtering Extension for Flask / SQLAlchemy

[![Build Status](https://travis-ci.org/exleym/Flask-Filter.svg?branch=master)](https://travis-ci.org/exleym/Flask-Filter)

# Introduction
Flask-Filter is a simple [Flask](http://flask.pocoo.org/) extension for
standardizing behavior of REST API resource search endpoints. It is
designed to integrate with the [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
extension and [Marshmallow](https://marshmallow.readthedocs.io/en/3.0/),
a popular serialization library.

Out-of-the-box, Flask-Filter provides search functionality on top-level
object fields via an array of filter objects provided in the JSON body
of a POST request. For configuring filtering on derived or nested fields
see the "Filtering on Nested Fields" section of the documentation.

# Default Filters
Flask-Filter supports searching resources based on an array of filters,
JSON objects with the following structure:

```json
{"field": "<field_name>", "op": "<operator>", "value": "<some_value>"}
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

Note: Be careful with typing around comparator operators. This version
does not provide rigorous type-checking, which could cause problems for
a user who submits a search like "find Pets with name greater than
'Fido'"

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


### Example 3: Initializing and using the Flask extension object

```python
from flask import Flask

from pet_store import Pet, PetSchema  # Model defined as subclass of `db.Model`
from pet_store.extensions import db, filtr  # SQLAlchemy and FlaskFilter objects

app = Flask(__name__)
db.init_app(app)
filtr.init_app(app)


@app.route('/api/v1/pets/search', methods=['POST']
def pet_search():
    pets = filtr.search(Pet, request.json.get("filters"), PetSchema)
    return jsonify(pet_schema.dump(pets)), 200
```

or alternatively, if you pre-register the Model and Schema with the
`FlaskFilter` object you do not need to pass the `Schema` directly to
the `search` method:

```python
filtr.register_model(Dog, DogSchema)  # Register in the app factory
```

followed by the search execution (without an explicitly-defined schema):

```python
pets = filtr.search(Pet, request.json.get("filters"))
```
