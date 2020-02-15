from django.shortcuts import render
from .models import course, assType, assignment
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'grades/index.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return course.objects.all()