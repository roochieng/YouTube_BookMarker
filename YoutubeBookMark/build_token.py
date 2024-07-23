import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_credentials():
    creds = None
    token_path = 'my_file.json'
    credentials_path = 'YoutubeBookMark/my_cred_file.json'

    # Print the current working directory
    print(f"Current working directory: {os.getcwd()}")

    # Check if the credentials file exists
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found: {credentials_path}")

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

if __name__ == "__main__":
    creds = get_credentials()
    print("Credentials obtained successfully!")
