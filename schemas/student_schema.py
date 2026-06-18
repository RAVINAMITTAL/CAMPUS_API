from marshmallow import Schema, fields

class StudentSchema(Schema):

    name = fields.Str(required=True)

    email = fields.Email(required=True)

    department_id = fields.Int(required=True)

    