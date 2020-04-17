from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
import google.oauth2.credentials
import google_auth_oauthlib.flow
import iso8601
import pytz
from django.utils.timezone import localtime
# import dateutil.parser
from django.http import HttpResponse
from django.conf import settings
from django.utils.safestring import mark_safe
import os
from .models import *
from .utils import Calendar

from .forms import *
from django.contrib.auth.models import User

#from here
import datetime
from datetime import datetime, date
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#to here, this came from https://developers.google.com/calendar/quickstart/python
#and I'm not sure it's right for this place
SCOPES = ['https://www.googleapis.com/auth/calendar']
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
    calendar_list = service.calendarList().list(pageToken = None).execute()
    e = []
    for calendar_ID in calendar_list['items']:
        
        # if(calendar_ID.get('selected') is True or calendar_ID.get('accessRole') == 'reader'):
        if(calendar_ID.get('selected') is True):
            events_result = service.events().list(calendarId=calendar_ID['id'], timeMin=now,
                                                singleEvents=True,
                                                orderBy='startTime').execute()
            # if(events_result is not None):
            events = events_result.get('items',[])
       

            for event in events:
                # print(event)
                e.append(event)
    # events = events_result.get('items', [])
    eventlist = []

    for event in e:
        # localtime(event.start_time)
        start = event['start'].get('dateTime', event['start'].get('date'))
     
       
        end = event['end'].get('dateTime', event['end'].get('date'))
        # localtime(start)
        # print(start)
        # localtime(start)
        endtime = iso8601.parse_date(end)
        
        starttime = iso8601.parse_date(start)
        # print(starttime)
        # localtime(endtime.start_time)
        # localtime(starttime.start_time)
        print(starttime)
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


# tutorial followed by https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month'))
        # print(self.request.GET.get('day'))

        
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, user = self.request.user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        #context['event'] = Event.objects.filter(owner=self.request.user)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    # days_in_month = calendar.monthrange(d.year, d.month)[1]
    days_per_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if(d.year % 4 == 0):
        days_per_month[2] = 29
    days_in_month = days_per_month[d.month]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
def deleteall(request):
    events = Event.objects.filter(owner = request.user)
    events.delete()
    return HttpResponseRedirect(reverse('index2'))
def delete_event(request, event_id):
    event = Event.objects.get(id = event_id)
    event.delete()
    return HttpResponseRedirect(reverse('index2'))
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        title = request.POST.get('title')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        endtime = iso8601.parse_date(end)
        # localtime(start.start_time)
        starttime = iso8601.parse_date(start)
        
        startminute = str(starttime.minute).zfill(2)
        endminute = str(endtime.minute).zfill(2)
        
        startmonth = starttime.strftime("%B")
        if(event_id is None):
            Event.objects.create(title = title, owner=request.user,start_time = start, end_time = end, start_month_name = startmonth, from_google = False, startminute = startminute, endminute = endminute)
        else:
            instance.title = title
            instance.start_time = start
            instance.end_time = end
            instance.start_month_name = startmonth
            instance.startminute = startminute
            instance.endminute = endminute
            instance.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'calendar/event.html', {'form': form})