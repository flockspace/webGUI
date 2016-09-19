'''
Created on 09-Aug-2016

@author: suhaheer

User registration backend
'''


import uuid
import datetime

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext
from django.template.response import TemplateResponse
from django.template import Template, Context
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
#User = get_user_model()
from webApp.models import user_model as User
#from django.template.context_processors import request
#from webApp.forms import UserLoginForm, UserCreateForm
#from django.contrib.auth.forms import UserCreationForm

from django.views.decorators.csrf import csrf_exempt
from __builtin__ import True
#from aetypes import template

exception=''

def checkUserExistence(registered):
    try:
        obj = User.objects.exclude().filter(username=registered['username']).exists()
        if obj:
            print "Username exists. Please choose a different one."
            global exception
            exception="Username exists. Please choose a different one."
            return True
        else:
            return False
    except Exception as err:
        print "Exception occurred while validating user existence"
        global exception
        exception="Exception occurred while validating user existence"
        raise Exception(err)
        return True
    

def validate_registration_attributes(registered):
    try:
        if not (registered['first_name'] and registered['last_name'] and 
                registered['email'] and registered['username'] and 
                registered['passwd_1'] and registered['passwd_2']):
            global exception
            exception="All fields must be filled!"
            return False
        
        if((registered['passwd_1']!=registered['passwd_2']) or 
            (registered['passwd_1']==None) or (registered['passwd_1']=='')):
            global exception
            exception="Both passwords must be same and can not be empty"
            return False
            #validate emailID
            #validate userID
    except Exception as err:
        global exception
        exception="Validation of input fields failed. Please enter them again."
        raise Exception("""EXCEPTION at validate_registration_attributes in 
        userObject.py:%s""" % (err))
        return False
    
    if checkUserExistence(registered):
        return False
    return True

  
def register(request):
    if request.method=='POST':
        if validate_registration_attributes(request.POST):
            user_uuid = uuid.uuid4()
            try:
                user = User.objects.create(user_id=user_uuid,
                                        last_login=str(datetime.datetime.now()),
                                        username= request.POST['username'],
                                        first_name= request.POST['first_name'],
                                        last_name= request.POST['last_name'],
                                        email= request.POST['email'],
                                        profile_pic = "blank_image.png",
                                        banner_pic = "blank_image.png",
                                        password = '',
                                        )
                user.set_password(request.POST['passwd_1'])
                user.save()
                #Registration was successful. Logging in the user.
                login(request,user)
                return HttpResponseRedirect('/home',"Successfully registered")
            except Exception as err:
                user.delete()
                raise Exception("""EXCEPTION at register-user.objects.create in 
                                userObject:%s""" % (err))
                return HttpResponseRedirect('/register','''Exception occurred 
                                            at user registration''')
        else:
            print "New account registration form validation failed"
            context={'RegisterResponse':exception}
            return render(request, 'welcome.html', context)
            
    else:
        print "Invalid HTTP method used for Form registration"
        return HttpResponseRedirect('/welcome','''Invalid http method used for 
                                    registration''')
    
