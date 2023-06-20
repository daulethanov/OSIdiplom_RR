from application.database.client import db


class Idea(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String())
    image = db.relationship('ImageUpload', backref='ideas', cascade='all, delete-orphan')




