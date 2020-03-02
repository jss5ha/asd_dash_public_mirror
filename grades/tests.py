from django.test import TestCase
from django.urls import reverse
from .models import course
# Create your tests here.

def create_course(course_text):
    return course.objects.create(course_name = course_text)


class CourseTests(TestCase):
    def test_no_course(self):
        response = self.client.get(reverse('grades:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please log in to see your Personal Dashboard")
        self.assertQuerysetEqual(response.context['course_list'], [])
    def test_add_course(self):
        create_course('course1')
        response = self.client.get(reverse('grades:index'))
        self.assertQuerysetEqual(
            response.context['course_list'],
            ['<course: course1>']
        )
    def test_add_course_null(self):
        create_course('')
        response = self.client.get(reverse('grades:index'))
        self.assertQuerysetEqual(
            response.context['course_list'],
            ['<course: >']
        )
    def test_add_course_2(self):
        create_course('a')
        response = self.client.get(reverse('grades:index'))
        self.assertQuerysetEqual(
            response.context['course_list'],
            ['<course: a>']
        )
    def test_authentication(self):
        response = self.client.get(reverse('grades:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertQuerysetEqual(response.context['course_list'], [])

