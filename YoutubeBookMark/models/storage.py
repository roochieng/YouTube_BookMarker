from config import db, login_manager, migrate, app
from datetime import datetime,timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    An object to create new and manage users in the database

    Args:
        db: database model
        UserMixin (_type_): _Flask method to support with Logins
        and account creations_
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    bookmarks = db.relationship('BookMarks', backref='author', lazy=True)


    @staticmethod
    def get_token(self, expires_sec=1800):
        serial = Serializer(app.secret_key, expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')
    

    @staticmethod
    def verify_token(token):
        serial = Serializer(app.secret_key)
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self, email, password, date_created) -> None:
        self.email = email
        self.password = password
        self.date_created = datetime.now(timezone.utc)

    def __repr__(self):
        return(f"User('{self.email}' '{self.date_created}')")

class BookMarks(db.Model):
    """
    Object for storing bookmark

    Args:
        db: database model
    """
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(250), nullable=False)
    video_name = db.Column(db.String(120), nullable=False)
    channel_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, video_url, video_name, channel_name, date_created, user_id=User.id) -> None:
        self.video_url = video_url
        self.video_name = video_name
        self.channel_name = channel_name
        self.user_id = user_id
        self.date_created = datetime.now(timezone.utc)


    def __repr__(self):
        return(f"BookMarks ('{self.video_url}', '{self.video_name}', '{self.channel_name}', '{self.date_created}')")
