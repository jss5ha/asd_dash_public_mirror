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
        self.assertContains(response, "No classes have been created.")
        self.assertQuerysetEqual(response.context['course_list'], [])
    def test_add_course(self):
        create_course('course1')
        response = self.client.get(reverse('grades:index'))
        self.assertQuerysetEqual(
            response.context['course_list'],
            ['<course: course1>']
        )


