from datetime import timedelta
class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
    SECRET_KEY = "123"
    JWT_SECRET_KEY = "123"
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = 'uploads'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=64)
