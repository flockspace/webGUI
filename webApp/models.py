from __future__ import unicode_literals

# Create your database models here

from django.contrib.auth.models import User, AbstractBaseUser
from django.db import models
import time
import os.path
import imghdr


def upload_location(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    newname=instance.uuid.split('-')[-1]
    newname+=str((time.time()))
    ext = imghdr.what(instance.profile_pic)
    return "%s/%s.%s" %(instance.uuid, newname, ext.lower())

class user_model(AbstractBaseUser):
    uuid = models.CharField(max_length=50, primary_key=True)
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
    workEmail = models.EmailField()
    last_login = models.CharField(max_length=50,default="None")
    profile_pic = models.ImageField(width_field=None,height_field=None,
                                    blank=True,default="None",
                                    upload_to=upload_location)
    
    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS = ['uuid']
    
    class Meta:
        db_table='user_model'
        app_label='webApp'


class workprofile_model(AbstractBaseUser):
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
