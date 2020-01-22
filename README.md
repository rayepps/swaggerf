# OpenAPI Spec Builder
Python library used to generate swagger docs from decorators. Doesn't screw with your requests, doesn't alter your middleware, doesn't put its dirty little hands where they don't belong. You decorate functions, register them on a schema, and generate a swagger doc.

## Install
Use `PyPI` -> `oapispec` @ https://pypi.org/project/oapispec

## Getting Started

In this example `mock_schema` is a `dict` that is a valid OpenAPI spec and can be written to a file as json.
```
from http import HTTPStatus

import oapispec as oapi

schema = oapi.schema(metadata=dict(
    version='4.2.0',
    title='Super API'
))

@oapi.doc.namespace('Health Check')
@oapi.doc.route('/ping')
@oapi.doc.method('GET')
def ping():
    pass

mock_schema = schema.register(ping)
```

### Creating Models
In this example we create a model and use it as an expected parameter to a `POST` request.
```
book_model = oapi.model.Model('Book', {
    'title': oapi.fields.String(required=True),
    'author': oapi.fields.String(required=True),
    'yearWritten': oapi.fields.String,
    'genre': oapi.fields.String,
    'edition': oapi.fields.Integer,
    'isInPrint': oapi.fields.Boolean
})

@oapi.doc.namespace('Book')
@oapi.doc.route('/book')
@oapi.doc.method('POST')
@oapi.doc.response(HTTPStatus.CREATED.value, HTTPStatus.CREATED.description, book_model)
@oapi.doc.expect(book_model)
def add_book():
    pass

mock_schema = schema.register(add_book)
```