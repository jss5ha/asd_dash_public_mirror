from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
import google.oauth2.credentials
import google_auth_oauthlib.flow
import iso8601
import pytz
# import dateutil.parser
from django.http import HttpResponse
from django.conf import settings
from django.utils.safestring import mark_safe
import os
from .models import *
from .utils import Calendar
from django.contrib.auth.models import User

#from here
from datetime import datetime 
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#to here, this came from https://developers.google.com/calendar/quickstart/python
#and I'm not sure it's right for this place
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# Create your views here.
# https://stackoverflow.com/questions/48242761/how-do-i-use-oauth2-and-refresh-tokens-with-the-google-api
if settings.TEST_SERVER is True:
    REDIRECT_URI = "https://localhost:8000/calendar/events"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
else:
    REDIRECT_URI = "https://asd-dash.herokuapp.com/calendar/events"
class IndexView(generic.ListView):
    template_name = 'calendar/index.html'
    context_object_name = 'event'
    def get_queryset(self):
        if not (self.request.user.is_anonymous):
            return Event.objects.filter(owner=self.request.user)
        else:
            return Event.objects.none()
    # def list_calendar(self):
    #     #SOURCE: this code comes from https://developers.google.com/calendar/quickstart/python
    #     creds = None
    #     # The file token.pickle stores the user's access and refresh tokens, 
    #     # and is created automatically when the authorization flow completes 
    #     # for the first time.
    #     # if os.path.exists('token.pickle'):
    #         # with open('token.pickle', 'rb') as token:
    #             # creds = pickle.load(token)
    #     # If there are no (valid) credentials available, let the user log in.
    #     if not creds or not creds.valid:
    #         if creds and creds.expired and creds.refresh_token:
    #             creds.refresh(Request())
    #         else:
    #             flow = InstalledAppFlow.from_client_secrets_file(
    #                 'credentials.json', SCOPES)
    #             creds = flow.run_local_server(port=0)
    #         # Save the credentials for the next run
    #         with open('token.pickle', 'wb') as token:
    #             pickle.dump(creds, token)

    #     service = build('calendar', 'v3', credentials=creds)

    #     # Call the Calendar API
    #     now = datetime.datetime.utcnow().isoformat()
    #     events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    #     events = events_result.get('items', [])
    #     if not events:
    #         print('No upcoming events found.')
    #     for event in events:
    #         start = event['start'].get('dateTime', event['start'].get('date'))
    #         print(start, event['summary'])

        #I'm not sure if it's okay for this to not return 
        # anything so I'm trying it
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json', SCOPES)
flow.redirect_uri = REDIRECT_URI

def authorize(request):
    # https://developers.google.com/identity/protocols/oauth2/web-server
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json', SCOPES)
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(access_type = 'offline', include_granted_scopes='true')
    return HttpResponseRedirect(authorization_url)


# https://www.geeksforgeeks.org/python-django-google-authentication-and-fetching-mails-from-scratch/
# https://stackoverflow.com/questions/48242761/how-do-i-use-oauth2-and-refresh-tokens-with-the-google-api
def main(request):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    state = request.GET.get('state', None)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json', scopes=None, state=state)
    flow.redirect_uri = REDIRECT_URI
    authorization_response = request.build_absolute_uri()
    # print(authorization_response)
    flow.fetch_token(authorization_response = authorization_response)
    credentials = flow.credentials
    service = build('calendar', 'v3', credentials=credentials)
    for e in Event.objects.all():
        if e.from_google is True:
            e.delete()
    # creds = None
    # The file token.pickle stores the user's access and r   efresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.pickle'):
        # with open('token.pickle', 'rb') as token:
            # creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         # flow = InstalledAppFlow.from_client_secrets_file(
    #         #     'credentials.json', SCOPES)
    #         # creds = flow.run_local_server(port=0)
    #         # creds = os.path.join(BASE_DIR, 'credentials.json')
    #         # authorization_response = input('https://localhost:8000/')
    #         # creds = flow.fetch_token(authorization_response = authorization_response)
    #     # Save the credentials for the next run
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)
    # print("ok")
    # service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
  
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    eventlist = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
     
       
        end = event['end'].get('dateTime', event['end'].get('date'))
        endtime = iso8601.parse_date(end)
        
        starttime = iso8601.parse_date(start)
       
        #https://medium.com/@pritishmishra_72667/converting-rfc3339-timestamp-to-utc-timestamp-in-python-8dfa485358ff

        startminute = str(starttime.minute).zfill(2)
        endminute = str(endtime.minute).zfill(2)
        
        eventdetails = []
        eventdetails.append(event['summary'])
        startmonth = starttime.strftime("%B")
        Event.objects.create(title = event['summary'], owner= request.user, start_time = starttime, end_time = endtime, start_month_name = startmonth, from_google = True, startminute = startminute, endminute = endminute)
        #add a user to the event here?
        eventlist.append(eventdetails)
     
        
    # return HttpResponseRedirect(reverse('index'))
    context = {'eventlist': eventlist, 'event': Event.objects.filter(owner=request.user)}
    template = 'calendar/index.html'
    return HttpResponseRedirect(reverse('index2'))



class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()