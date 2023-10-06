from __future__ import print_function

from os.path import exists
from pathlib import Path
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# TODO indicator that try to connect
# TODO handle scenario then gen token is not ended properlly
def find_calendar_id(service):
    """
    Iter through calendars in Google Calendar.\n
    If calendar with name is found THEN return calendar id ELSE return None
    """
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == 'Timer':
                return calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            return None

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def add_to_google_calendar(db_path: Path, static_path: Path, name: str, date: str, start_time: str, duration: int, desc: str) -> tuple[int, str]:
    '''
    Add action to google calendar, through google calendar api.
    Returns a tuple with int that represents whether the event was successfully added 
    and str that is either a link to the event or an error code.
    '''
    creds = None
    token_path = db_path / 'token.json'
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                static_path / 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        id = find_calendar_id(service)
        if not id:
            calendar = {
                'summary': 'Timer'
            }
            created_calendar =service.calendars().insert(body=calendar).execute()
            id = created_calendar['id']

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

        event = service.events().insert(calendarId=id, body=event).execute()
        return (1, event.get('htmlLink'))

    except HttpError as error:
        return (0, error)