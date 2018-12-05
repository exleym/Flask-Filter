
from setuptools import setup

setup(
    name='Flask-Filter',
    version='0.1dev',
    packages=['flask_filter',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "marshmallow", "sqlalchemy", "Flask-SQLAlchemy"],
)
