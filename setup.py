
from setuptools import find_packages, setup

setup(
    name='Flask-Filter',
    version='0.1.2a3',
    author="Exley McCormick",
    author_email="exleym@gmail.com",
    description="A Flask extension for creating standard resource searches",
    packages=find_packages(exclude=["tests", "docs", "contrib"]),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/exleym/Flask-Filter ",
    install_requires=[
      "flask", "marshmallow", "sqlalchemy", "Flask-SQLAlchemy"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "marshmallow", "sqlalchemy", "Flask-SQLAlchemy"],
)
