from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

import iso8601
import pytz
# import dateutil.parser
from django.http import HttpResponse

from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar

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
class IndexView(generic.ListView):
    template_name = 'calendar/index.html'
    # context = list_calendar()
    def get_queryset(self):
        return Event.objects.all()
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
    for e in Event.objects.all():
        if e.from_google is True:
            e.delete()
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
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     'credentials.json', SCOPES)
            # creds = flow.run_local_server(port=0)
            cred = os.path.join(settings.BASE_DIR, 'credentials.json')
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
  
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    eventlist = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(event['start'])
        # parsedDate = dateutil.parser.parse(start)
        # print(parsedDate)
        # date = datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%d-%z")
        end = event['end'].get('dateTime', event['end'].get('date'))
        endtime = iso8601.parse_date(end)
        # print(date)
        starttime = iso8601.parse_date(start)
        # starttime = starttime.replace(tzinfo=None)
        #https://medium.com/@pritishmishra_72667/converting-rfc3339-timestamp-to-utc-timestamp-in-python-8dfa485358ff

        startminute = str(starttime.minute).zfill(2)
        endminute = str(endtime.minute).zfill(2)
        
        eventdetails = []
        eventdetails.append(event['summary'])
        startmonth = starttime.strftime("%B")
        Event.objects.create(title = event['summary'], start_time = starttime, end_time = endtime, start_month_name = startmonth, from_google = True, startminute = startminute, endminute = endminute)
        eventlist.append(eventdetails)
        print(start, event['summary'])
        
    # return HttpResponseRedirect(reverse('index'))
    context = {'eventlist': eventlist, 'event': Event.objects.all()}
    template = 'calendar/index.html'
    return render(request, template, context)


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