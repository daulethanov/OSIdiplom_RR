from marshmallow import Schema, fields


class IdeaSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    image = fields.Nested('ImageUploadSchema', exclude=('problem_id', ), many=True)
