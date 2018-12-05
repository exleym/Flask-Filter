# Flask-Filter
Filtering Extension for Flask / SQLAlchemy


# Examples
This section demonstrates a couple use-cases for Flask-Filter

```python
from flask import Flask, jsonify, request
from flask_filter import apply_filters

app = Flask(__name__)

@app.route('/api/v1/pets/search', methods=['POST'])
def pet_search():
    filters = request.json.get("filters")
```