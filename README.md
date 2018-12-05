# Flask-Filter
Filtering Extension for Flask / SQLAlchemy


# Examples
This section demonstrates a couple use-cases for Flask-Filter

### Example 1: Manually implementing filters in a flask view
Using the `FilterSchema` class directly, you can deserialize an
array of JSON filters into a list of `flask_filter.Filter` objects
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
