from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views import generic

from .models import course
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'grades/index.html'
    context_object_name = 'test'

    def get_queryset(self):
        return 