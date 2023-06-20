from marshmallow import Schema, fields


class OLXSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    number = fields.Str()
    price = fields.Int()
    user_id = fields.Integer()
    image = fields.Nested('ImageUploadSchema',exclude=('olx_id', ), many=True)



class OLXWithImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    number = fields.String()
    price = fields.Integer()
    image_id = fields.Integer()
    user_id = fields.Integer()



class ProblemSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    number = fields.Integer()
    iin = fields.String()
    title = fields.String()
    description = fields.String()
    create_at = fields.DateTime()
    finish = fields.DateTime()
    price = fields.Integer()
    completed = fields.Boolean()
    act_job = fields.String()
    level_problem = fields.String()
    whatsapp = fields.Integer()
    image = fields.Nested('ImageUploadSchema',exclude=('problem_id', ), many=True)


class ImageUploadSchema(Schema):
    id = fields.Integer(dump_only=True)
    fileName = fields.String()
    file = fields.String()
    problem_id = fields.Integer()
    olx_id = fields.Integer()
    idea_id = fields.Integer()