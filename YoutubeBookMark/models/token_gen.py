from itsdangerous import URLSafeTimedSerializer
from ..config import app, mail
from flask import url_for
from flask_mail import Message


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email




def send_confirmation_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = f'<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p><p><a href="{confirm_url}">{confirm_url}</a></p>'
    subject = "Please confirm your email"
    msg = Message(subject=subject, recipients=[user_email], html=html)
    mail.send(msg)