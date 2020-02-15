from django.shortcuts import render
from .models import course, assType, assignment
from django.urls import reverse
from django.views import generic
# Create your views here.

class gradeHomeView(generic.ListView):
    template_name = 'grades/courses.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return course.objects.all()