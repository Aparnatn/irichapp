# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.db.models import fields
from django.forms import widgets
from authentication import models
from authentication.models import deals, mobile, rewards
from authentication.models import business_details,category,payments,roles
from authentication.forms import mobile

class MobileLoginForm(forms.Form):
     phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
class Meta:
        model = mobile
        fields = ('sId','phone',)

class BusinessForm(forms.Form):
   
    class Meta:
        model = business_details
        fields = "__all__"
class dealsForm(forms.Form):
   
    class Meta:
        model = deals
        fields = "__all__"
       
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "form-control"
            }
        ))


class paymentForm(forms.ModelForm):
  class Meta:
    model=payments
    fields ="__all__"
class rolesForm(forms.ModelForm):
  class Meta:
    model=roles
    fields ="__all__"        


class business_detailsForm(forms.ModelForm):

    class Meta:
        model = business_details
        
        fields = "__all__"
class categoryForm(forms.ModelForm):

    class Meta:
        model = category
        fields ='__all__'
class rewardsForm(forms.ModelForm):

    class Meta:
        model = rewards
        fields ='__all__'


    

