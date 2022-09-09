Changelog
=========
The Change Log for this project contains all meaningful changes to the function
of the code base. It does not necessarily include changes to the form of the
code, i.e. refactoring.

* PENDING (v0.1.2): support comparative datetimes and complete migration
  from Travis CI to GitHub Actions.

* 2022-09-08 (v0.1.1): support nullable equals and not-equals operators and
  move off of Travis CI and onto GitHub Actions. This update was created
  to resolve an issue reported by @topermaper

* 2020-09-08 (v0.1.0dev5): added support for Marshmallow 2, along with a
  deprecation warning that it will be removed in future versions. This was
  implemented via a deserializer function located in the "schemas" module.
