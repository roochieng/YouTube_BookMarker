from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import json
from ..config import app


# Define the scopes required by the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_credentials():
    creds = None
    token_path = 'my_token_file.json'
    credentials_path = 'my_file.json'

    if os.path.exists(token_path):
        with open(token_path, 'r') as token:
            creds_data = json.load(token)
            if all(k in creds_data for k in ('client_id', 'client_secret', 'refresh_token', 'token')):
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
            else:
                print("Token file is missing required fields. Please reauthorize.")
    else:
        print("Token file not found. Please reauthorize.")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    return creds


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
    
    # Create the email message
    message = {
        'raw': create_message('me', user_email, subject, html)
    }
    
    # Send the email using Gmail API
    try:
        service = build('gmail', 'v1', credentials=get_credentials())
        service.users().messages().send(userId='me', body=message).execute()
        print(f'Successfully sent confirmation email to {user_email}')
    except HttpError as error:
        print(f'An error occurred: {error}')

def create_message(sender, to, subject, body):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64
    
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(body, 'html')
    message.attach(msg)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return raw_message
