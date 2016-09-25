'''
Created on 22-Aug-2016

@author: suhaheer

User authentication backend
'''


import uuid
import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
#User = get_user_model()
from webApp.models import user_model as User
from webApp.messageHandler import AMQHandler as AMQ

#from django.template.context_processors import request
#from webApp.forms import UserLoginForm, UserCreateForm
#from django.contrib.auth.forms import UserCreationForm

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def profileLogin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            userObj = User.objects.get(username=username)
        except Exception as err:
            print ("Authentication error:%s" % (err))
            return HttpResponseRedirect('/welcome','User authentication failed. Login again')
        
        if userObj.check_password(password):
            if userObj.is_active and userObj.is_authenticated():
                login(request, userObj)
                '''Although queue and default subscription worked during 
                registration, doing again doesn't affect.
                '''
                amqp = AMQ(userObj.user_id)
                return HttpResponseRedirect('/home','Successfull login. Redirecting to home page.')
            else:
                print "User account is not active."
                return HttpResponseRedirect('/welcome','User account is not active. Create new account')
        else:
            print "User authentication failed."
            return HttpResponseRedirect('/login','User authentication failed. Login again')
        
    else:
        print "Wrong HTTP method is used for authentication!."
        return HttpResponseRedirect('/welcome','Wrong HTTP method is used for authentication!')

     
def profileLogout(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/welcome','Successfully logged out')
    else:
        logout(request)
        print "ERROR:Unauthorized request"
        return HttpResponseRedirect('/welcome','Forcibly logged out')
        