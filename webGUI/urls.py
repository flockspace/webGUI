"""webGUI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

"""
Static files related imports
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from django.contrib import admin

from webApp.views import profileView, welcomeView, userAuth , userActivities
from webApp.views import profileUpdates, contentManager, userRegister

urlpatterns = [
    url(r'^$', welcomeView.welcome, name='welcome'),
    url(r'^welcome', welcomeView.welcome, name ='welcome'),
    url(r'^login', userAuth.profileLogin, name='login'),
    url(r'^logout', userAuth.profileLogout, name='logout'),
    
    url(r'^register', userRegister.register, name='register'),
    
    url(r'^home', profileView.home, name='home'),
    url(r'^about', profileView.about, name='about'),
    url(r'^view', profileView.view_profile, name='about'),
    
    url(r'^change_profile_pic', profileUpdates.update_profile_pic, name='change_profile_pic'),
    url(r'^change_banner_pic', profileUpdates.update_banner_pic, name='change_banner_pic'),
    url(r'^update_profile', profileUpdates.update_profile, name='update_profile'),
    
    url(r'^activities', userActivities.activities, name='activities'),
    url(r'^content_deletion', userActivities.generic_content_deletion, name='content_deletion'),
    
    url(r'^upload_content', contentManager.contentManager, name='upload_content'),
]
if settings.DEBUG==True:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)