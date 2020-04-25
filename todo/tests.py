from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from .models import Todo
from django.contrib.auth.models import User
from .views import index, deleteAll


# Create your tests here.

def create_todo(thing, user):
    return Todo.objects.create(text=thing, owner=user, complete=False, due_date="2000-01-01", group='School')


# class todo_tests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='test')
#         self.user2 = User.objects.create_user(username='loser')

#     def test_connection(self):
#         create_todo('task', self.user)
#         request = self.factory.get('/todo/index.html')
#         request.user = self.user
#         response = index(request)
#         self.assertEqual(response.status_code, 200)


# class MoreTodoTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='test')
#         self.user2 = User.objects.create_user(username='loser')

#     def test_user_grade(self):
#         create_todo('task', self.user)
#         request = self.factory.get('/todo/index.html')
#         request.user = self.user
#         response = index(request)
#         # print(response.content)
#         c = Client()
#         # print(c.get('/todo/index.html'))
#         c.post('/login/?visitor=true', {'name': 'fred', 'passwd': 'secret'})
#         response = c.get('/todo/')
#         # print(response.context)
#         # print(response)
#         # print(Todo.objects.get_queryset())
#         # print((response.content.__contains__('task'.encode())))
#         self.assertQuerysetEqual(
#             Todo.objects.get_queryset(),
#             ['<Todo: task>']
#         )
#         # self.assertTrue(response.context['todo_list'] == 'task')
#         # self.assertEqual(response.content.__contains__('task'.encode()), True)

#     def test_not_user_grade(self):
#         create_todo('task1', self.user)
#         request = self.factory.get('/todo/index.html')
#         request.user = self.user2
#         response = index(request)
#         self.assertEqual(response.content.__contains__(''.encode()), True)

#     def test_del_grade(self):
#         create_todo('task2', self.user)
#         request = self.factory.get('/todo/index.html')
#         request.user = self.user
#         response = deleteAll(request)
#         self.assertEqual(response.content.__contains__('task2'.encode()), False)