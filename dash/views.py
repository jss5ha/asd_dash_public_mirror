from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.views.decorators.http import require_POST
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

class AuthRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/') # or http response
        return None