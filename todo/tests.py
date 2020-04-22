from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Todo
from django.contrib.auth.models import User
from .views import index, deleteAll
# Create your tests here.

def create_todo(thing, group,user):
    return Todo.objects.create(text=thing, group=group ,owner=user)

class todo_tests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test')
        self.user2 = User.objects.create_user(username='loser')

    def test_connection(self):
        create_todo('task', 'School',self.user)
        request = self.factory.get('/todo/index.html')
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)

class MoreTodoTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'test')
        self.user2 = User.objects.create_user(username = 'loser')


    def test_user_grade(self):
        create_todo('task', 'School', self.user)
        request = self.factory.get('/todo/index.html')
        request.user = self.user
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['todo_list'], 'task')

    def test_not_user_grade(self):
        create_todo('task1', 'School',self.user)
        request = self.factory.get('/todo/index.html')
        request.user = self.user2
        response = index(request)
        self.assertEqual(response.content.__contains__(''.encode()), True)

    def test_del_grade(self):
        create_todo('task2','School',self.user)
        request = self.factory.get('/todo/index.html')
        request.user = self.user
        response = deleteAll(request)
        self.assertEqual(response.content.__contains__('task2'.encode()), False)
