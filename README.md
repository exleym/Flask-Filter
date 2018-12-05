# Flask-Filter
Filtering Extension for Flask / SQLAlchemy

[![Build Status](https://travis-ci.org/exleym/Flask-Filter.svg?branch=master)](https://travis-ci.org/exleym/Flask-Filter)

# Introduction
TODO: put an introduction here!


# Examples
This section demonstrates a couple use-cases for Flask-Filter

### Example 1: Manually implementing filters in a flask view
Using the `FilterSchema` class directly, you can deserialize an
array of JSON filters into a list of `flask_filter.Filter` objects
and directly apply the filters using `Filter.apply` to craft a
SQLAlchemy query with a complex set of filters.

```python
from flask import Flask, jsonify, request
from flask_filter import FilterSchema

from pet_store.schemas import PetSchema

app = Flask(__name__)
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
from flask import Flask, jsonify, request
from flask_filter import query_with_filters

from pet_store.schemas import PetSchema

app = Flask(__name__)
pet_schema = PetSchema()

@app.route('/api/v1/pets/search', methods=['POST']
def pet_search():
    pets = query_with_filters(Pet, request.json.get("filters"), PetSchema)
    return jsonify(pet_schema.dump(pets)), 200
```