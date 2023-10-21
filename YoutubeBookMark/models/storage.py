from collections.abc import Mapping, Sequence
from config import db
from datetime import datetime
from flask import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import MySQLdb.cursors

# Base = declarative_base()


class User(db.Model, UserMixin):
    """An object o create new and manage users in the database

    Args:
        db (_type_): database model
        UserMixin (_type_): _Flask method to support with Logins
        and account creations_
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime)
    bookmarks = db.relationship('BookMarks', backref='author', lazy=True)

    def __repr__(self):
        return(f"User('{self.email}'")

class BookMarks(db.Model):
    """Object for storing bookmark

    Args:
        db (_type_): _database method_
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    channel_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(f"BookMarks('{self.title}', '{self.channel_name}', '{self.date_created}'")