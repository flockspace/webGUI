'''
Created on 17-Sep-2016

@author: suhaheer
'''
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from django.template.context_processors import request
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect

from webApp.models import user_model as User
from webApp.models import contentSystems as Contents
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
def populate_audio_files(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
            audio_files = Contents.objects.filter(user=user.user_id,type="audio")
            return audio_files
        except Exception as err:
            print "Exception occurred while accessing DB with " \
                    "message %",err
            return failed_context
        pass
    else:
        return failed_context
    
def populate_video_files(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
            video_files = Contents.objects.filter(user=user.user_id,type="video")
            return video_files
        except Exception as err:
            print "Exception occurred while accessing DB with " \
                    "message %",err
            return failed_context
        pass
    else:
        return failed_context
    
def populate_image_files(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
            image_files = Contents.objects.filter(user=user.user_id,type="image")
            return image_files
        except Exception as err:
            print "Exception occurred while accessing DB with " \
                    "message %",err
            return failed_context
        pass
    else:
        return failed_context
    
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
            audioFiles = populate_audio_files(request, username)
            videoFiles = populate_video_files(request, username)
            imageFiles = populate_image_files(request, username)
            context['Content_images'] = imageFiles
            context['Content_videos'] = videoFiles
            context['Content_audios'] = audioFiles
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

'''Generic content deletion 
'''
def generic_content_deletion(request):
   
    if request.user.is_authenticated():
        if request.POST['button']=='image':
            delete_imgContent(request)
        elif request.POST['button']=='audio':
            delete_audioContent(request)
        elif request.POST['button']=='video':
            delete_videoContent(request)
        else:
            context = populate_user_context(request, request.user.username)
            return redirect('/activities',context,'unknown content deletion'\
                                        ' request')
        context = populate_user_context(request, request.user.username)
        return redirect('/activities',context,'Render after deletion')
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)

def delete_imgContent(request):
    
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        images = request.POST.getlist('imgContent_deletion')
        for id in images:
            Contents.objects.filter(content_id=id).delete()
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)

def delete_audioContent(request):
    
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        audio = request.POST.getlist('audioContent_deletion')
        for id in audio:
            Contents.objects.filter(content_id=id).delete()
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)
    
def delete_videoContent(request):
   
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        video = request.POST.getlist('videoContent_deletion')
        for id in video:
            Contents.objects.filter(content_id=id).delete()
    else:
        return HttpResponseRedirect('/welcome','User authentication failed. Login again')
    return HttpResponse(200)