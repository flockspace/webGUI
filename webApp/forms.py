'''
Created on 22-Aug-2016

@author: suhaheer
'''

from django.contrib.auth.models import User
from django import forms

class UserCreateForm(forms.Form):
    import pdb
    pdb.set_trace()
    username = forms.CharField(label ='username', max_length=30, value='suhas')
    email = forms.EmailField(label ='email', max_length=254, value='suhas@gmail.com')
    password1 = forms.CharField(label ='passwd_1',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label ='passwd_2',
                        widget=forms.PasswordInput())
    first_name = forms.CharField(label ='first_name')
    last_name = forms.CharField(label ='last_name')

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')


class UserLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
        
