from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

def home(request):
    return render(request, 'home.html')