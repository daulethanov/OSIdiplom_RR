from datetime import datetime
from .enum import UserPermission
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_security import SQLAlchemySessionUserDatastore, UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    role_user = db.Column(db.String())
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.BigInteger(), unique=True)
    active = db.Column(db.Boolean(), default=1)
    full_address = db.Column(db.String())
    apartment = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.now())
    number = db.Column(db.String())
    reset_password_code = db.Column(db.Integer())
    dom = db.Column(db.String())
    kv = db.Column(db.String())
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    problem = db.relationship("Problem", backref=db.backref('users'))
    performance = db.relationship("Performance", backref=db.backref('users'))
    idea = db.relationship("Idea", backref=db.backref('users'))
    olx = db.relationship("OLX", backref=db.backref('users'))
    category = db.relationship('Category', backref='users', cascade='all, delete-orphan')

    def __repr__(self):
        return self.email

    def password_hash(password):
        return generate_password_hash(password)

    def password_check_hash(self, password):
        return check_password_hash(self.password, password)

    def create_user(self, user):
        db.session.add(user)
        db.session.commit()

    def create_token(self, identity, id):
        token_payload = {
            'identity': identity,
            'id': id
        }
        access_token = create_access_token(identity=token_payload)
        return access_token


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


roles_users = db.Table(
    'roles_users',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
