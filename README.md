# Flask-Filter
Filtering Extension for Flask / SQLAlchemy


# Examples
This section demonstrates a couple use-cases for Flask-Filter

```python
from flask import Flask, jsonify, request
from flask_filter import apply_filters

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
