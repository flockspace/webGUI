'''
Created on 09-Aug-2016

@author: suhaheer
'''
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from django.template.context_processors import request
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
# Create your views here.


def welcome(request):
    return render(request, "welcome.html", None, "Content-type: text/HTML", 200, None)
    #return HttpResponse("<html><body><h2>Welcome to the Django project</h2><body></html>")