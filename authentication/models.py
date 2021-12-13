# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import random
from django.db import models
import base64
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import os
from .models import User
import json
from geopy.geocoders import Nominatim
from django.db.models import Sum, F
from django.db.models.signals import post_save
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import uuid
from .managers import GeneralManager
crontab = {}

from django.dispatch import receiver
CURRENCY = '€'

class Users(models.Model):
    username=models.CharField(max_length=150)
   
    email=models.CharField(max_length=150) 
    password1=models.CharField(max_length=150)
    password2=models.CharField(max_length=150)
    referral_code=models.CharField(max_length=150)
    
    phone=models.CharField(max_length=150)
    lastname=models.CharField(max_length=150)
    postcode=models.CharField(max_length=150)

class PaymentMethod(models.Model):
    title = models.CharField(unique=True, max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '0. Payment Method'



class Transactions(models.Model):      
        price = models.CharField(max_length=200)
        session_id = models.CharField(max_length=200)
        Customer=models.CharField(max_length=200)
        status = models.CharField(max_length=20,default='pending')
class Meta:
        verbose_name_plural = 'price'
def __str__(self):
        return self.price

    


class mobile(models.Model):
    sId=models.IntegerField()
    phone=models.CharField(max_length=50)
class business_details(models.Model):
    categories=models.ForeignKey(
        'category',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    bank_name=models.CharField(max_length=50)
    bsb=models.CharField(max_length=50)
    business_name=models.CharField(max_length=50)
    business_desc=models.CharField(max_length=200)
    business_address=models.CharField(max_length=200)
    email=models.EmailField(max_length=50)
    In=models.CharField(max_length=50)
    business_code=models.CharField(max_length=50)
    Account_holder=models.CharField(max_length=50)
    account_number=models.CharField(max_length=50)
    business_contact=models.CharField(max_length=50)
    image1= models.ImageField(upload_to='images',blank= True,null=True)
    add_offer=models.CharField(max_length=50)
    qr_code=models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        qrcode_image = qrcode.make(self.get_qr_url())
        canvas = Image.new("RGB", (400, 400), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr_code.save(f'code_{random.randint(0,9999)}.png', File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    def get_qr_url(self):
        return 'http://13.232.49.240:8000/payment.html'

    
        # return stream.getvalue().decode()
        
    # qrcode = property(_get_qrcode)

class category(models.Model):
    name=models.CharField(max_length=500)

class payments(models.Model):
    amount=models.IntegerField()
    business=models.ForeignKey(
        'business_details',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # verbose_name='business_name'
    )

# Create your models here.

# Create your models here.



# Create your models here.

