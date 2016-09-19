'''
Created on 17-Sep-2016

@author: suhaheer
'''
'''
Created on 30-Aug-2016

@author: suhaheer
'''

import uuid
import time
import datetime

from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from webApp.models import user_model as User
from webApp.views import profileView

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import imghdr

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

def update_profile(request):
    if request.user.is_authenticated():
        if request.method=='POST':
            new_dict = request.POST
            user = User.objects.get(username=request.user.username)
            user.email = ( new_dict['email'] or user.email or None)
            user.workEmail = ( new_dict['workEmail'] or user.workEmail or None)
            user.mobilePh = ( new_dict['mobilePh'] or user.mobilePh or None)
            user.workPh = ( new_dict['workPh'] or user.workPh or None)
            user.address = ( new_dict['livesIn'] or user.address or None)
            user.myself = ( new_dict['myself'] or user.myself or None)
            user.save()
            context = populate_user_context(request, user.username)
            return redirect("/about", context, "Content-type: text/HTML", 200, None)
        else:
            '''wrong http method is used.'''
            profileView.about(request)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)


def update_profile_pic(request):
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            user = User.objects.get(username=request.user.username)
            profile_pic =request.FILES.get('fileToUpload')
            if check_image_extension(profile_pic):
                user.profile_pic = profile_pic
                user.save()
                context = populate_user_context(request, request.user.username)
                return redirect("/home", context, "text/html", 200)
            else:
                context= populate_user_context(request, request.user.username)
                return redirect("/home", context, "text/html", 200)
        else:
            context= populate_user_context(request, request.user.username)
            return redirect("/home", context, "text/html", 200)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    
    return HttpResponse(200)

def update_banner_pic(request):
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            user = User.objects.get(username=request.user.username)
            banner_pic =request.FILES.get('fileToUpload')
            if check_image_extension(banner_pic):
                user.banner_pic = banner_pic
                user.save()
                context = populate_user_context(request, request.user.username)
                return redirect("/home", context, "text/html", 200)
            else:
                context= populate_user_context(request, request.user.username)
                return redirect("/home", context, "text/html", 200)
        else:
            context=populate_user_context(request, request.user.username)
            return redirect("/home", context, "text/html", 200)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    
    return HttpResponse(200)

def check_image_extension(filename):
    ext = imghdr.what(filename)
    if ext.lower() not in ['jpg','png','jpeg']:
        print "Image extension not supported"
        return False
    else:
        print "Image extension found:",ext.lower()
        return True