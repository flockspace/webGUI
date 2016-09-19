'''
Created on 17-Sep-2016

@author: suhaheer
'''
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from django.template.context_processors import request
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect

from webApp.models import user_model as User
# Create your views here.

failed_context = {'first_name':None,
                  'last_name':None,
                  'email':None,
                  'workEmail':None,
                  'mobilePh':None,
                  'workPh':None,
                  'profile_pic':None,
                  'banner_pic':None,
                  'myself':None,
                  'livesIn':None
                }

'''A generic method, Always pass the username to generate context'''
def populate_user_context(request,username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
            context={'first_name':(user.first_name or None),
                     'last_name':(user.last_name or None),
                     'email':(user.email or None),
                     'workEmail':(user.workEmail or None),
                     'mobilePh':(user.mobilePh or None),
                     'workPh':(user.workPh or None),
                     'profile_pic':(user.profile_pic or None),
                     'banner_pic':(user.banner_pic or None),
                     'myself':(user.myself or None),
                     'livesIn':(user.address or None)
                     }
            return context
        except Exception as err:
            return failed_context
    else:
        return failed_context


def activities(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        context = populate_user_context(request, user.username)
        return render(request, "activities.html", context, "Content-type: text/HTML", 200, None)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)
    