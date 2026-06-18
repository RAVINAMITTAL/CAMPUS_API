from marshmallow import Schema, fields, validate
# Summary: A lightweight library for converting complex datatypes to and from native Python datatypes.
class RegisterSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3,max=50)
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=6)
    )
    
class LoginSchema(Schema):

    username = fields.Str(required=True)

    password = fields.Str(required=True)    

    