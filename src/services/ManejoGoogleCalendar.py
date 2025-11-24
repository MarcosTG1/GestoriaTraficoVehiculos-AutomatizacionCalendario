import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config import GOOGLE_CREDENTIALS_PATH, GOOGLE_TOKEN_PATH

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Get paths from config module
CREDENTIALS_FILE = GOOGLE_CREDENTIALS_PATH
TOKEN_FILE = GOOGLE_TOKEN_PATH

def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Returns the service object.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"Credentials file not found at {CREDENTIALS_FILE}. Please follow the setup guide.")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

def list_upcoming_events(service, max_results=10):
    """Lists the next n upcoming events on the user's primary calendar."""
    import datetime
    
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print(f"Getting the upcoming {max_results} events")
    
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return []

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
    
    return events

def add_event(service, summary, start_time, end_time, description=None, location=None, recurrence=None):
    """Adds a new event to the primary calendar."""
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time, # ISO format: '2023-05-28T09:00:00-07:00'
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Madrid',
        },
    }
    
    if recurrence:
        event['recurrence'] = recurrence

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
    return event

def delete_event(service, event_id):
    """Deletes an event by ID."""
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Event {event_id} deleted.")
    except HttpError as e:
        print(f"An error occurred: {e}")
