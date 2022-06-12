from marshmallow import Schema, fields

# Product Schema
class ProductGetSchema(Schema):
    name = fields.Str(example="string")

class ProductPostSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    price = fields.Str(doc="price", example="int", required=True)
    amount = fields.Str(doc="amount", example="int", required=True)
    

class ProductPatchSchema(Schema):
    name = fields.Str(doc="name", example="string")
    price = fields.Str(doc="price", example="int")
    amount = fields.Str(doc="amount", example="int")
    

# Cart Schema

class CartPostSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    name = fields.Str(doc="name", example="string", required=True)
    amount = fields.Str(doc="amount", example="int", required=True)
    price = fields.Str(doc="price", example="int")

class CartPatchSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    name = fields.Str(doc="name", example="string", required=True)
    amount = fields.Str(doc="amount", example="int", required=True)
    price = fields.Str(doc="price", example="int")

class CartGetSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)   

# Response
class ProductGetResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())


class ProductCommonResponse(Schema):
    message = fields.Str(example="success")


