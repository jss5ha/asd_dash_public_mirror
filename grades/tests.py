from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import course
from django.contrib.auth.models import User
from .views import IndexView
# Create your tests here.

def create_course(course_text):
    return course.objects.create(course_name = course_text)

def create_course_with_user(course_text,user):
    return course.objects.create(course_name = course_text, owner = user)


class CourseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'test')
        self.user2 = User.objects.create_user(username = 'loser')

    def test_no_course(self):
        request = self.factory.get('/grades')
        request.user = self.user2
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            []
        )

    def test_add_grade(self):
        create_course_with_user('course', self.user)
        request = self.factory.get('/grades')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            ['<course: course>']
        )

    def test_add_course_null(self):
        create_course_with_user('', self.user)
        request = self.factory.get('/grades')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            ['<course: >']
        )
    def test_add_course_2(self):
        create_course_with_user('course1', self.user2)
        request = self.factory.get('/grades')
        request.user = self.user2
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            ['<course: course1>']
        )
    def test_authentication(self):
        request = self.factory.get('/grades')
        request.user = self.user2
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            []
        )

class usertests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'test')
        self.user2 = User.objects.create_user(username = 'loser')

    def test_user_grade(self):
        create_course_with_user('user_owned', self.user)
        request = self.factory.get('/grades')
        request.user = self.user
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            ['<course: user_owned>']
        )

    def test_dont_see_other_grades(self):
        create_course_with_user('user_owned', self.user)
        request = self.factory.get('/grades')
        request.user = self.user2
        view = IndexView()
        view.setup(request=request)
        context = view.get_queryset()
        self.assertQuerysetEqual(
            context,
            []
        )