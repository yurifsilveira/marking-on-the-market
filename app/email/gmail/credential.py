from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from os import path, environ
from logging import info
from dotenv import load_dotenv
load_dotenv()

SCOPES = ['https://mail.google.com/']
TOKEN = environ['PATH_TOKEN']
print(TOKEN)
imap_server  = "imap.gmail.com"

def get_credentials():
    creds = None
    
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(TOKEN, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    info("credenciais gmail geradas!")
    return creds
