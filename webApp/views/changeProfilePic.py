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

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import imghdr

def update_pro_pic(request):
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            user = User.objects.get(username=request.user.username)
            user.profile_pic =request.FILES.get('fileToUpload')
            if check_image_extension(user.profile_pic):
                user.save()
                context = {'image_id':user.profile_pic}
                return redirect("/home", context, "text/html", 200)
            else:
                context=None
                return redirect("/home", context, "text/html", 200)
        else:
            context=None
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