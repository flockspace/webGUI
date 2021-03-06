'''
Created on 10-Sep-2016

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
from webApp.models import album as album_table
from webApp.models import contentSystems as content_table
from webApp.messageHandler import AMQHandler as AMQ

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import imghdr


''' Methods and class definitions
'''
def check_image_extension(filename):
    ext = imghdr.what(filename)
    if ext.lower() not in ['jpg','png','jpeg','gif']:
        print "Image extension not supported"
        return False
    else:
        print "Image extension found:",ext.lower()
        return True

def check_extension(content):
    if 'image' in content.content_type:
        return True
    elif 'audio' in content.content_type:
        return True
    elif 'video' in content.content_type:
        return True
    else:
        return False

def upload_images(request):
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            user = User.objects.get(username=request.user.username)
            imageContent =request.FILES.get('imageContent')
            if check_extension(imageContent):
                content_entry = content_table.objects.create(content_id=uuid.uuid4(),
                                                         user_id=str(request.user.pk),
                                                         type="image",
                                                         category = "entertainment",
                                                         description=request.POST['img_description'],
                                                         title=request.POST['heading'],
                                                         location=''
                                                         )
                content_entry.location=request.FILES['imageContent']
                content_entry.save()
                
                "Publish content to all recipient "
                content =populate_AMQ_message(user,content_entry)
                amqp= AMQ(user.user_id)
                amqp.publish(content)
                
            else:
                context=populate_user_context(request, request.user.username)
                return redirect("/activities", context, "text/html", 200)
        else:
            context=populate_user_context(request, request.user.username)
            return redirect("/home", context, "text/html", 200)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    
    return HttpResponse(200)
    
def upload_audio(request):  
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            user = User.objects.get(username=request.user.username)
            audioContent =request.FILES.get('audioContent')
            if check_extension(audioContent):
                content_entry = content_table.objects.create(content_id=uuid.uuid4(),
                                                         user_id=str(request.user.pk),
                                                         type="audio",
                                                         category = "entertainment",
                                                         description=request.POST['audio_description'],
                                                         title=request.POST['heading'],
                                                         location=''
                                                         )
                content_entry.location=request.FILES['audioContent']
                content_entry.save()
                "Publish content to all recipient "
                content =populate_AMQ_message(user,content_entry)
                amqp= AMQ(user.user_id)
                amqp.publish(content)
                
            else:
                context=populate_user_context(request, request.user.username)
                return redirect("/activities", context, "text/html", 200)
        else:
            context=populate_user_context(request, request.user.username)
            return redirect("/home", context, "text/html", 200)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    
    return HttpResponse(200)

def upload_video(request):
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            user = User.objects.get(username=request.user.username)
            videoContent =request.FILES.get('videoContent')
            if check_extension(videoContent):
                content_entry = content_table.objects.create(content_id=uuid.uuid4(),
                                                         user_id=str(request.user.pk),
                                                         type="video",
                                                         category = "entertainment", 
                                                         description=request.POST['video_description'],
                                                         title=request.POST['heading'],
                                                         location=''
                                                         )
                content_entry.location=request.FILES['videoContent']
                content_entry.save()
                
                "Publish content to all recipient "
                content =populate_AMQ_message(user,content_entry)
                amqp= AMQ(user.user_id)
                amqp.publish(content)
                
            else:
                context=populate_user_context(request, request.user.username)
                return redirect("/activities", context, "text/html", 200)
        else:
            context=populate_user_context(request, request.user.username)
            return redirect("/home", context, "text/html", 200)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    
    return HttpResponse(200)

def contentManager(request):
    if request.user.is_authenticated() and request.method=='POST':
        if 'portfolio-album' in request.POST.keys() and request.POST['portfolio-album']=='Submit':
            upload_portfolio_album(request)
        elif 'image' in request.POST.keys() and request.POST['image']=='Submit':
            upload_images(request)
        elif 'audio' in request.POST.keys() and request.POST['audio']=='Submit': 
            upload_audio(request)
        elif 'video' in request.POST.keys() and request.POST['video']=='Submit':
            upload_video(request)
        else:
            print "unverified input type"

        context = populate_user_context(request, request.user.username)
        return redirect("/activities", context, "text/html", 200)
        
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    
    return HttpResponse(200)

def upload_portfolio_album(request):
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            user = User.objects.get(username=request.user.username)
            user.profile_pic =request.FILES.get('portfolioContent')
            if check_image_extension(user.profile_pic):
                user.save()
                context = populate_user_context(request, request.user.username)
                return redirect("/activities", context, "text/html", 200)
            else:
                context=populate_user_context(request, request.user.username)
                return redirect("/home", context, "text/html", 200)
        else:
            context=None
            return redirect("/home", context, "text/html", 200)
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    
    return HttpResponse(200)


'''A generic method, Always pass the username to generate context'''
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

def populate_AMQ_message(user,content_entry):
    msg = { "content_id":str(content_entry.content_id or None),
            "content_type":str(content_entry.type or None),
            "content_location":str(content_entry.location or None),
            "content_category":str(content_entry.category or None),
            "content_description":str(content_entry.description or None),
            "content_title":str(content_entry.title or None),
            
            "user_id":str(user.user_id or None),
            "user_uname":str(user.username or None),
            "user_fname":str(user.first_name or None),
            "user_lname":str(user.last_name or None),
            "user_email":str(user.email or None),
            "user_workEmail":str(user.workEmail or None),
            "user_mobilePh":str(user.mobilePh or None),
            "user_workPh":str(user.workPh or None),
            "user_profile_pic":str(user.profile_pic or None),
            "user_banner_pic":str(user.banner_pic or None),
            "user_myself":str(user.myself or None),
            "user_livesIn":str(user.address or None)
           }
    return msg  
            
            