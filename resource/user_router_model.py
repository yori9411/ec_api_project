from marshmallow import Schema, fields


# Schema
class UserGetSchema(Schema):
    name = fields.Str(example="string")

class UserPostSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    gender = fields.Str(doc="gender", example="string", required=True)
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)
    birth = fields.Str(doc="birth", example="string")
    note = fields.Str(doc="note", example="string")

class UserPatchSchema(Schema):
    name = fields.Str(doc="name", example="string")
    gender = fields.Str(doc="gender", example="string")
    account = fields.Str(doc="account", example="string")
    password = fields.Str(doc="password", example="string")
    birth = fields.Str(doc="birth", example="string")
    note = fields.Str(doc="note", example="string")

class LoginSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)

# Response
class UserGetResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())


class UserCommonResponse(Schema):
    message = fields.Str(example="success")


