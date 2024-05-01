from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from app import db


class AuthUser(db.Model, UserMixin):
    __tablename__ = "auth_users"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password
