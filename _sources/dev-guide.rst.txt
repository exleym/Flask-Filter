Developer's Guide
=================
This section will outline the tools and processes used to maintain the
project and ensure seamless publication of changes and improvements to
the Python Package Index for easy installation with Pip.

Testing
-------
Testing is currently being done in old-style unittest.TestCase
classes. Need to modernize this to pytest at some point. The tests
reside in a top-level ``tests/`` directory and rely on a simple
"MiniPet" pet-store application. This app has data-models and schemas,
but basically nothing else (not even endpoints right now).

Test coverage is calculated using the coverage module of Pytest, and a
coverage badge is generated and hosted by `Coveralls`_.


Building with Travis
--------------------
The CI process for this library is run through travis.org. Thanks
to the folks over at Travis CI for hosting open-source projects for
free.

* `Travis CI Build Dashboard`_
* `Travis Build Config`_

On pushing a commit to GitHub, Travis CI kicks off a build that runs
tests, checks coverage, and pushes badge info where it needs to go.

Deploying built Packages to PyPI
--------------------------------
Currently, this part of the CI / CD process is not automated. To publish
a feature / fix / change to  PyPI as a new version of the library, you have
to manually increment the build number, build the shippable package, and
publish it to Test PyPI and followed by Prod PyPI. This section outlines
the requirements to publish a release and provides some links. The
`Python Packaging User Guide`_ provided by the Python Packaging Authority
(PyPA) has everything you need to know, but the quick-and-dirty is here:

1. Increment the distribution version in both the ``__version__`` variable
   in the top-level ``__init__.py`` and in ``setup.py``
2. Build the project locally, saving output to the ``dist/`` directory.

    ``$ python setup.py sdist bdist_wheel``

3. Push these packages to Test PyPI.

    ``$ python -m twine upload --repository testpypi dist/*``

4. Check that the pushed libraries work and can be installed via pip.
5. Push the validated packages to Production PyPI.

    ``$ python -m twine upload dist/*``

Both steps (3) and (5) will prompt you for your username and password,
which are different for the production and test instances of PyPI.


.. _Travis CI Build Dashboard: https://travis-ci.org/github/exleym/Flask-Filter
.. _Travis Build Config: https://github.com/exleym/Flask-Filter/blob/master/.travis.yml
.. _Python Packaging User Guide: https://packaging.python.org/tutorials/packaging-projects/
.. _Coveralls: https://coveralls.io/github/exleym/Flask-Filter?branch=master
