from __future__ import unicode_literals

# Create your database models here

from django.contrib.auth.models import User, AbstractBaseUser
from django.db import models
import time
import os.path
import imghdr


def upload_profile_pic(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/profile_pic/<filename>
    newname=instance.user_id.split('-')[-1]
    newname+=str((time.time()))
    ext = imghdr.what(instance.profile_pic)
    if ext is None:
        ext='jpeg'
    return "%s/%s/%s.%s" %(instance.user_id, "profile_pic" ,newname, ext.lower())

def upload_banner_pic(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/banner_pic/<filename>
    newname=str(instance.pk).split('-')[-1]
    newname+=str((time.time()))
    ext = imghdr.what(instance.banner_pic)
    if ext is None:
        ext='jpeg'
    return "%s/%s/%s.%s" %(instance.user_id, "banner_pic" ,newname, ext.lower())

def content_upload_audio(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<audio>/<filename>
    newname=str(instance.pk).split('-')[-1]
    newname+=str((time.time()))
    ext = imghdr.what(instance.location)
    if ext is None:
        ext='mp3'
    return "%s/%s/%s.%s" %(instance.user_id, "audio", newname, ext.lower())

def content_upload_video(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<video>/<filename>
    newname=str(instance.pk).split('-')[-1]
    newname+=str((time.time()))
    ext = imghdr.what(instance.location)
    if ext is None:
        ext='mp4'
    return "%s/%s/%s.%s" %(str(instance.user_id), "video", newname, ext.lower())

def content_upload_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<image>/<filename>
    newname=str(instance.pk).split('-')[-1]
    newname+=str((time.time()))
    ext = imghdr.what(instance.location)
    if ext is None:
        ext='jpeg'
    return "%s/%s/%s.%s" %(str(instance.user_id),"images",newname, ext.lower())

def upload_generic(instance, filename):
    #Generic call for finding type of file.
    if(instance.type=='image'):
        return content_upload_image(instance, filename)
    elif(instance.type=='audio'):
        return content_upload_audio(instance, filename)
    elif(instance.type=='video'):
        return content_upload_video(instance, filename)
    else:
        return "None"


class user_model(AbstractBaseUser):
    user_id = models.CharField(max_length=50, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50,default="None")
    last_name = models.CharField(max_length=50,default="None")
    email = models.EmailField(default="None")
    password = models.CharField(max_length=150,default="abc123")
    
    '''Custom user information fields. '''
    myself = models.CharField(max_length=300,default="None")
    address = models.CharField(max_length=300,default="None")
    mobilePh = models.CharField(max_length=20,default="None")
    workPh = models.CharField(max_length=20,default="None")
    workEmail = models.EmailField(default="None")
    last_login = models.CharField(max_length=50,default="None")
    profile_pic = models.ImageField(width_field=None,height_field=None,
                                    blank=True,default="None",
                                    upload_to=upload_profile_pic)
    banner_pic = models.ImageField(width_field=None,height_field=None,
                                    blank=True,default="None",
                                    upload_to=upload_banner_pic)
    
    
    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS = ['user_id']
    
    class Meta:
        db_table='user_model'
        app_label='webApp'


class workprofile_model(models.Model):
    workId = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey('user_model', on_delete=models.CASCADE,
                             default="None")
    designation = models.CharField(default="None",max_length=50)
    organization = models.CharField(default="None",max_length=50)
    period = models.CharField(default="None",max_length=50)
    description = models.CharField(default="None",max_length=200)
    
    REQUIRED_FIELDS = ['workId']
    
    class Meta:
        db_table='workprofile_model'
        app_label='webApp'
        

class album(models.Model):
    user = models.ForeignKey('user_model', on_delete=models.CASCADE,
                             default="None")
    album_id = models.CharField(max_length=50,default="None")
    description = models.CharField(max_length=500,default="None")
    
    REQUIRED_FIELDS = ['album_id']
    class Meta:
        db_table='album'
        app_label='webApp'

class contentSystems(models.Model):
    content_id = models.CharField(max_length=50,primary_key=True)
    user = models.ForeignKey('user_model', on_delete=models.CASCADE,
                             default="None")
    type = models.CharField(max_length=10,default="None") #images,audio,video
    category = models.CharField(max_length=30,default="None") #??
    description = models.CharField(max_length=500,default="None")
    location = models.FileField(blank=True,default="None",
                                upload_to=upload_generic)
    
    REQUIRED_FIELDS = ['content_id']
    
    class Meta:
        db_table='contentSystems'
        app_label='webApp'
     
