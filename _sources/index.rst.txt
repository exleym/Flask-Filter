.. Flask-Filter documentation master file, created by
   sphinx-quickstart on Thu Dec 20 08:32:01 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-Filter: A simple search extension
=======================================
Flask-Filter provides a simple extension to the Flask web framework that
provides detailed search functionality for REST APIs.

The search functionality turns a JSON list of `Filter` objects of the form

`{"field": "name", "op": "=", "value": "Fido"}`

into chained filters on a SQLAlchemy query. By leveraging the great work done
by the SQLAlchemy and Marshmallow teams, we are able to easily provide a
standardized search function to REST APIs.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   documentation/source/tutorial



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
