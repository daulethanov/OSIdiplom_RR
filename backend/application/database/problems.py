import datetime
from application.database.client import db
from application.database.enum import ActJob, LevelProblem


class Problem(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.Integer(), primary_key=True)
    iin = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    number = db.Column(db.Integer())
    title = db.Column(db.String())
    description = db.Column(db.String())
    create_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    finish = db.Column(db.DateTime())
    price = db.Column(db.Integer())
    completed = db.Column(db.Boolean(), default=0)
    act_job = db.Column(db.Enum(ActJob), default=ActJob.pending)
    level_problem = db.Column(db.Enum(LevelProblem), default=LevelProblem.minimal)
    whatsapp = db.Column(db.Integer())
    image = db.relationship('ImageUpload', backref='problems', cascade='all, delete-orphan')

    def __repr__(self):
       return self.number


class Performance(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    title = db.Column(db.String())
    description = db.Column(db.String())

    def __repr__(self):
        return self.id


class ImageUpload(db.Model):
    __tablename__ = 'image_upload'
    id = db.Column(db.Integer(), primary_key=True)
    fileName = db.Column(db.String())
    file = db.Column(db.String(), nullable=True)
    olx_id = db.Column(db.Integer(), db.ForeignKey('olx.id'))
    problem_id = db.Column(db.Integer(), db.ForeignKey('problem.id'))
    idea_id = db.Column(db.Integer(),  db.ForeignKey('idea.id'))

    def __repr__(self):
        return self.file


class OLX(db.Model):
    __tablename__ = 'olx'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String)
    title = db.Column(db.String)
    number = db.Column(db.String)
    price = db.Column(db.Integer)
    image = db.relationship('ImageUpload', backref='olx', cascade='all, delete-orphan')

    def __repr__(self):
        return self.title






