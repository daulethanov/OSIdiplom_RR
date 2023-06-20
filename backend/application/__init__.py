from flask import Flask
from flask_jwt_extended import JWTManager
from flask_security import Security
from flask_migrate import Migrate
from application.OLX.idea.view import idea
from application.OLX.problem import problem
from application.OLX.view import olx
from application.admin.adminDashboard import admin
from application.client.view import auth, docs
from application.config.Base import Config
from application.database.client import db
from flask_cors import CORS


def init_app(app):
    JWTManager(app)
    Security(app)
    admin.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    CORS(app, resources={r"*": {"origins": "*"}})



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(auth)
    app.register_blueprint(olx)
    app.register_blueprint(problem)
    app.register_blueprint(idea)
    docs.init_app(app)
    return app
