from marshmallow import Schema , fields


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()


class UserSchema(Schema):
    id = fields.Integer()
    iin = fields.String()
    role_user = fields.String()
    full_name = fields.String()
    apartment = fields.String()
    email = fields.String()
    password = fields.String()
    token = fields.Integer()
    active = fields.Boolean()
    created_at = fields.DateTime()
    number = fields.String()
    reset_password_code = fields.Integer()
    roles = fields.Nested(RoleSchema(many=True))

