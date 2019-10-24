
from setuptools import setup

setup(
    name='Flask-Filter',
    version='0.1dev',
    author="Exley McCormick",
    author_email="exleym@gmail.com",
    description="A Flask extension for creating standard resource searches",
    packages=['flask_filter',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/exleym/Flask-Filter",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "marshmallow", "sqlalchemy", "Flask-SQLAlchemy"],
)
