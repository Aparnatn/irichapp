# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import widgets
from authentication.models import mobile
from authentication.models import business_details,category
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
    category = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    bank_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    bsb = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    business_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    business_desc = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    business_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    In = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    subcategory = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    Account_holder = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
    account_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "phone",
                "class": "form-control"
            }
        ))
class Meta:
        model = business_details
        fields = ('category','account_number','Account_holder','subcategory', 'In','email','business_address','business_desc','business_name','bsb','business_contact')
       
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Firstname",
                "class": "form-control"
            }
        ))
    lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Lastname",
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",
                "class": "form-control"
            }
        ))
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Mobile",
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
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",
                "class": "form-control"
            }
        ))
    customercode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "customer code",
                "class": "form-control"
            }
        ))
    communitycode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "community code",
                "class": "form-control"
            }
        ))
    salescode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "sales code",
                "class": "form-control"
            }
        ))
    class Meta:
        model = User
        fields = '__all__'


class business_detailsForm(forms.ModelForm):

    class Meta:
        model = business_details
        fields ='__all__'
        # fields = ('category','account_number','Account_holder','subcategory', 'Abin','email','business_address','business_desc','business_name','bsb','bank_name','image1')
class categoryForm(forms.ModelForm):

    class Meta:
        model = category
        fields ='__all__'


    

