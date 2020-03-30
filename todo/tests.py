from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Todo
from django.contrib.auth.models import User
from .views import index
# Create your tests here.

def create_todo(thing,user):
    return Todo.objects.create(text = thing, owner=user)

class todo_tests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'test')
        self.user2 = User.objects.create_user(username = 'loser')

    def test_user_grade(self):
        create_todo('task', self.user)
        request = self.factory.get('/todo/index.html')
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code,200)
'''        context = response.context['todo_list']
        self.assertQuerysetEqual(
            context,
            ['<Todo: task>']
        )'''