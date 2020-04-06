from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

#from here
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#to here, this came from https://developers.google.com/calendar/quickstart/python
#and I'm not sure it's right for this place
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'calendar/index.html'
    # context = list_calendar()
    def get_queryset(self):
        return 
    def list_calendar(self):
        #SOURCE: this code comes from https://developers.google.com/calendar/quickstart/python
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, 
        # and is created automatically when the authorization flow completes 
        # for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat()
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        #I'm not sure if it's okay for this to not return 
        # anything so I'm trying it


def main(request):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return HttpResponseRedirect(reverse('index'))


# def google_calendar_connection():
#         """
#         This method used for connect with google calendar api.
#         """
        
#         flags = tools.argparser.parse_args([])
#         FLOW = OAuth2WebServerFlow(
#             client_id='xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com',
#             client_secret='xxxxxx',
#             scope='https://www.googleapis.com/auth/calendar',
#             user_agent='<application name>'
#             )
#         storage = Storage('calendar.dat')
#         credentials = storage.get()
#         if credentials is None or credentials.invalid == True:
#             credentials = tools.run_flow(FLOW, storage, flags)
        
#         # Create an httplib2.Http object to handle our HTTP requests and authorize it
#         # with our good Credentials.
#         http = httplib2.Http()
#         http = credentials.authorize(http)
#         service = discovery.build('calendar', 'v3', http=http)
        
#         return service