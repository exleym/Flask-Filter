from .schemas import FilterSchema


filter_schema = FilterSchema()


def query_with_filters(class_, filters, schema=None):
    _filters = filter_schema.load(filters, many=True)
    query = class_.query
    for f in _filters:
        query = f.apply(query, class_, schema)
    return query.all()
