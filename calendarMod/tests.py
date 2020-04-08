from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Event
from django.contrib.auth.models import User
from .views import IndexView
# Create your tests here.

def create_event(title, start_time, end_time, start_month_name, from_google, startminute, endminute):
    return Event.objects.create(title = title,  start_time = start_time, end_time = end_time, start_month_name = start_month_name, from_google = from_google, startminute = startminute, endminute = endminute)

def create_event_with_user(title, description, start_time, end_time, start_month_name, from_google, startminute, endminute ,user):
    return Event.objects.create(title = title,  start_time = start_time, end_time = end_time, start_month_name = start_month_name, from_google = from_google, startminute = startminute, endminute = endminute, owner = user)


class CourseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'test')
        self.user2 = User.objects.create_user(username = 'loser')

    def test_no_event(self):
        request = self.factory.get('/grades')
        request.user = self.user2
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            []
        )

    def test_add_event(self):
        E = create_event('date', "2000-01-01 01:00", "2000-01-01 02:00", "May", False, "20", "20")
        request = self.factory.get('/calendar')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            ['<Event: date>']
        )
        

    def test_check_from_google(self):
        E = create_event('date',"2000-01-01 01:00", "2000-01-01 02:00", "May", False, "20", "20")
        request = self.factory.get('/calendar')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertFalse(E.from_google)

    def test_check_start_time(self):
        E = create_event('date', "2000-01-01 01:00", "2000-01-01 02:00", "May", False, "20", "20")
        request = self.factory.get('/calendar')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertTrue(E.start_time == "2000-01-01 01:00")
    
    def test_check_start_time2(self):
        E = create_event('date', "2000-01-01 01:00", "2000-01-01 02:00", "May", False, "20", "20")
        request = self.factory.get('/calendar')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertFalse(E.start_time == "2000-01-01 02:00")

    def test_check_end_time(self):
        E = create_event('date', "2000-01-01 01:00", "2000-01-01 02:00", "May", False, "20", "20")
        request = self.factory.get('/calendar')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertTrue(E.end_time == "2000-01-01 02:00")
    
    def test_check_month_name(self):
        E = create_event('date', "2000-01-01 01:00", "2000-01-01 02:00", "May", False, "20", "20")
        request = self.factory.get('/calendar')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertTrue(E.start_month_name == "May")
#https://stackoverflow.com/questions/6103825/how-to-properly-use-unit-testings-assertraises-with-nonetype-objects
    def test_add_event_improper_input(self):
        with self.assertRaises(TypeError):
            create_event('')
        request = self.factory.get('/grades')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            []
        )

    def test_add_event_then_add_improper(self):
        E = create_event('date', "2000-01-01 01:00", "2000-01-01 02:00", "May", False, "20", "20")
        with self.assertRaises(TypeError):
            create_event('')
        request = self.factory.get('/calendar')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            ['<Event: date>']
        )
        
        
