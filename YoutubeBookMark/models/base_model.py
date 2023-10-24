from collections.abc import Mapping, Sequence
from typing import Any
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, ValidationError, DataRequired, Email, EqualTo
from flask_login import login_user, login_required, logout_user, current_user
from models.storage import User, BookMarks
from email_validator import validate_email, EmailNotValidError
from pytube import YouTube, Playlist, Channel
from pytube.exceptions import VideoUnavailable


    
class RegistrationForm(FlaskForm):
    """ Registration method to allow user creat an account.
    Validates if the account meets the requirements, and creates the account

    Args:
        FlaskForm (_type_): _Flask Object to process user login_

    Raises:
        ValidationError: _Raises a validation error when the user registers
        with an email existing in the db_
    """
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired(),
                                         Length(min=6, max=20)],
                                    render_kw={"placeholder": "password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                    render_kw={"placeholder": "confirm password"})
    submit = SubmitField("Register")


    def validate_email(self, email):
        """validate user account creation by checking if email exists already

        Args:
            email (_type_): _parameter to check_

        Raises:
            ValidationError: _The error to raise if email exists_
        """
        try:
            valid = validate_email(email.data)
            email.data = valid.email
        except EmailNotValidError as e:
            raise ValidationError('Invalid email address')
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email address is registered, log in or register with another email')
        


class LoginForm(FlaskForm):
    """Login method from FlaskForm: validates and allows the user to log in

    Args:
        FlaskForm (_type_): _Flask Object to process user login_
    """
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()],
                                    render_kw={"placeholder": "password"})
    submit = SubmitField("Sign in")


class UrlBookmark(FlaskForm):
    url = StringField('Video url', validators=[DataRequired()],
                      render_kw={"placeholder": "youtube video url"})
    submit = SubmitField('Bookmark')