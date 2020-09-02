Tutorial
========
This will eventually be a tutorial for using Flask-Filter. Woot!


Using the FlaskFilter Extension
-------------------------------
The best way to use this library (when working with a normal Flask project) is
to use the ``FlaskFilter`` extension object. Typical use of this object (as
with all Flask extensions) is to instantiate a singleton object in an
``extensions.py`` module in your project. Register the extension in your
application factory, and then import the singleton wherever you need to
perform a filtered search.


.. code-block:: python

    from flask import Flask

    # Pet is a Model defined as subclass of db.Model
    # db is a SQLAlchemy and filter is a FlaskFilter object
    from pet_store import Pet, PetSchema
    from pet_store.extensions import db, filtr

    app = Flask(__name__)
    db.init_app(app)
    filtr.init_app(app)


    @app.route('/api/v1/pets/search', methods=['POST'])
    def pet_search():
        pets = filtr.search(Pet, request.json.get("filters"),
                            PetSchema)
        return jsonify(pet_schema.dump(pets)), 200



You may also pre-register the Model and Schema with the
`FlaskFilter` object, in which case you do not need to pass the `Schema`
directly to the `search` method. This may be useful if you are writing a lot
of search endpoints, but should usually be unnecessary.

.. code-block:: python

    # Register the model in your application factory (or wherever
    # you define your models)
    filtr.register_model(Dog, DogSchema)

    # Elsewhere in the application, you can search without a schema
    pets = filtr.search(Pet, request.json.get("filters"))


Ordering the Search Response
----------------------------
By default, searches return objects ordered on ``id``, ascending. This behavior
can be customized with the optional ``order_by`` argument.

If you don't have an ``id`` parameter for your database objects or you wish to
sort by other fields, you should populate the ``order_by`` argument to the
search function when you call it.

This approach does not allow API consumers to set the order_by argument, but
allows the developer to override the default id ordering.

.. code-block:: python

    @app.route('/api/v1/pets/search', methods=['POST'])
    def pet_search():
        pets = filtr.search(Pet, request.json.get("filters"),
                            PetSchema, order_by=Pet.name)
        return jsonify(pet_schema.dump(pets)), 200


Alternatively, if you wish to allow users to customize the order of the
objects in the response, use a string for the ``order_by`` argument.

.. code-block:: python

    @app.route('/api/v1/pets/search', methods=['POST'])
    def pet_search():
        order_by = json.get("orderBy") or "name"
        pets = filtr.search(Pet, request.json.get("filters"),
                            PetSchema, order_by=order_by)
        return jsonify(pet_schema.dump(pets)), 200