from __future__ import print_function

import os.path
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def add_to_google_calendar(name: str, date: str, start_time: str, duration: int, desc: str) -> tuple[int, str]:
    '''
    Add action to google calendar, through google calendar api.
    Returns a tuple with int that represents whether the event was successfully added 
    and str that is either a link to the event or an error code.
    '''
    print(name, date, start_time, duration, desc)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        end = (datetime.strptime(date + ' ' + start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=duration)).strftime('%Y-%m-%dT%H:%M:%S')
        event = {
        'summary': name,
        'description': desc,
        'start': {
            'dateTime': f"{date}T{start_time}+02:00",
        },
        'end': {
            'dateTime': f"{end}+02:00",
        },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return (1, event.get('htmlLink'))

    except HttpError as error:
        return (0, error)


if __name__ == '__main__':
    add_to_google_calendar()