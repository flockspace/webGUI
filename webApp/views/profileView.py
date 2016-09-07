'''
Created on 09-Aug-2016

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
                  'image_id':None,
                  'myself':None,
                  'address':None
                }

def home(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        context={'image_id':user.profile_pic}
        return render(request, "home_.html", context, "Content-type: text/HTML", 200, None)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')

def update_profile(request):
    if request.user.is_authenticated():
        if request.method=='POST':
            new_dict = request.POST
            user = User.objects.get(username=request.user.username)
            user.email = ( new_dict['email'] or user.email or None)
            user.workEmail = ( new_dict['workEmail'] or user.workEmail or None)
            user.mobilePh = ( new_dict['mobilePh'] or user.mobilePh or None)
            user.workPh = ( new_dict['workPh'] or user.workPh or None)
            user.address = ( new_dict['address'] or user.address or None)
            user.myself = ( new_dict['myself'] or user.myself or None)
            user.save()
            context = populate_user_context(request, user.username)
            return render(request, "about.html", context, "Content-type: text/HTML", 200, None)
        else:
            '''wrong http method is used.'''
            about(request)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)
    
def about(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        context = populate_user_context(request, user.username)
        return render(request, "about.html", context, "Content-type: text/HTML", 200, None)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)

def activities(request):
    return render(request, "activities.html", None, "Content-type: text/HTML", 200, None)

def view_profile(request):
    import pdb
    pdb.set_trace()
    if request.user.is_authenticated():
        if request.method=='GET':
            id=request.GET['id']
            user = User.objects.get(pk=id)
            context = populate_user_context(request, user.username)
            return render(request, "generic_profile.html", context, "Content-type: text/HTML", 200, None)
        else:
            print "Wrong http request method."
            return HttpResponseRedirect('/home','Wrong http request method.')
    else:
        print "User need to login"
        return HttpResponseRedirect('/welcome','User need to login')
    HttpResponse(200)

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
                     'image_id':(user.profile_pic or None),
                     'myself':(user.myself or None),
                     'address':(user.address or None)
                     }
            return context
        except Exception as err:
            return failed_context
    else:
        return failed_context