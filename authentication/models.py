# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
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
class User(models.Model):
    username=models.CharField(max_length=150)
    email=models.CharField(max_length=150) 
    password1=models.CharField(max_length=150)
    password2=models.CharField(max_length=150)
    communitycode=models.CharField(max_length=150)
    customercode=models.CharField(max_length=150)
    phone=models.CharField(max_length=150)
    lastname=models.CharField(max_length=150)
    salescode=models.CharField(max_length=150)

class PaymentMethod(models.Model):
    title = models.CharField(unique=True, max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '0. Payment Method'


class DefaultExpenseModel(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    date_expired = models.DateField()
    final_value = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    paid_value = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    is_paid = models.BooleanField(default=False)
    payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
    objects = models.Manager()
    my_query = GeneralManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_paid:
            self.paid_value = self.final_value
        else:
            self.paid_value = 0
        super(DefaultExpenseModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'

    tag_final_value.short_description = 'Value'

    def tag_is_paid(self):
        return 'Is Paid' if self.is_paid else 'Not Paid'

    tag_is_paid.short_description = 'Paid'

    @staticmethod
    def analysis(queryset):
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.filter(is_paid=False).aggregate(Sum('final_value'))['final_value__sum']\
            if queryset.filter(is_paid=False) else 0
        diff = total_value - paid_value
        category_analysis = queryset.values('category__title').annotate(total_value=Sum('final_value'),
                                                                       remaining=Sum(F('final_value')-F('paid_value'))
                                                                       ).order_by('remaining')
        return [total_value, paid_value, diff, category_analysis]

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        cate_name = request.GET.getlist('cate_name', None)
        paid_name = request.GET.getlist('paid_name', None)
        person_name = request.GET.getlist('person_name', None)

        queryset = queryset.filter(title__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(category__id__in=cate_name) if cate_name else queryset
        queryset = queryset.filter(is_paid=True) if 'paid' == paid_name else queryset.filter(is_paid=False)\
            if 'not_paid' == paid_name else queryset
        if person_name:
            try:
                queryset = queryset.filter(person__id__in=person_name)
            except:
                queryset = queryset
        return queryset


class BillCategory(models.Model):
    title = models.CharField(unique=True, max_length=150)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    class Meta:
        verbose_name_plural = '1. Bill Category'

    def __str__(self):
        return self.title

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'

    tag_balance.short_description = 'Value'

    def update_category(self):
        queryset = self.bills.all()
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] \
            if queryset.filter(is_paid=True) else 0
        self.balance = total_value - paid_value
        self.save()


class Bill(DefaultExpenseModel):
    category = models.ForeignKey(BillCategory, null=True, on_delete=models.SET_NULL, related_name='bills')

    class Meta:
        verbose_name_plural = '2. Bills'
        ordering = ['-date_expired']

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'{self.category.title} - {self.id}'
        super(Bill, self).save(*args, **kwargs)
        self.category.update_category()

    def tag_category(self):
        return f'{self.category}'


class PayrollCategory(models.Model):
    title = models.CharField(unique=True, max_length=150)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    class Meta:
        verbose_name_plural = '3. Payroll Category'

    def __str__(self):
        return self.title

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'

    tag_balance.short_description = 'Value'

    def update_category(self):
        queryset = self.category_payroll.all()
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] \
            if queryset.filter(is_paid=True) else 0
        self.balance = total_value - paid_value
        self.save()


class Person(models.Model):
    title = models.CharField(unique=True, max_length=150)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    class Meta:
        verbose_name_plural = '4. Persons'

    def __str__(self):
        return self.title

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'

    tag_balance.short_description = 'Value'

    def update_person(self):
        queryset = self.person_payroll.all()
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] \
            if queryset.filter(is_paid=True) else 0
        self.balance = total_value - paid_value
        self.save()


class Payroll(DefaultExpenseModel):
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL, related_name='person_payroll')
    category = models.ForeignKey(PayrollCategory, null=True, on_delete=models.SET_NULL, related_name='category_payroll')

    class Meta:
        verbose_name_plural = '5. Payroll'
        ordering = ['-date_expired']

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'{self.person.title} - {self.id}'
        super(Payroll, self).save(*args, **kwargs)
        self.person.update_person()
        self.category.update_category()

    def tag_category(self):
        return f'{self.person} - {self.category}'


class GenericExpenseCategory(models.Model):
    title = models.CharField(unique=True, max_length=150)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    class Meta:
        verbose_name_plural = '6. Expense Category'

    def __str__(self):
        return self.title

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'

    tag_balance.short_description = 'Value'

    def update_category(self):
        queryset = self.category_expenses.all()
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] \
            if queryset.filter(is_paid=True) else 0
        self.balance = total_value - paid_value
        self.save()


class GenericExpense(DefaultExpenseModel):
    category = models.ForeignKey(GenericExpenseCategory, null=True, on_delete=models.SET_NULL,
                                 related_name='category_expenses')

    class Meta:
        verbose_name_plural = '7. Generic Expenses'
        ordering = ['-date_expired']

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'{self.title}'
        super(GenericExpense, self).save(*args, **kwargs)
        self.category.update_category()

    def tag_category(self):
        return f'{self.category}'
class Transactions(models.Model):      
    contact = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    code = models.ImageField(upload_to='qr_codes', blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    item=models.ImageField(upload_to='qr_codes', blank=True)
    def save(self, *args, **kwargs):
        link =  'http://0.0.0.0:8000/api/v1/transaction/complete/'+self.uuid.hex+'/'
        qrcode_img = qrcode.make(link)       
        canvas = Image.new('RGB', (440,440), 'white')    
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.item}.png'
        buffer = BytesIO() 
        canvas.save(buffer,'PNG')
        self.code.save(fname,File(buffer), save=False) 
        canvas.close()
        super().save(*args, **kwargs)

class Restraunt(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=500)
    pincode = models.CharField(max_length=10)
    lat = models.CharField(max_length=20 , null=True , blank=True)
    lon = models.CharField(max_length=20 , null=True , blank=True)
    
    
    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(int(self.pincode))
        self.lat = location.latitude
        self.lon = location.longitude
        super(Restraunt, self).save(*args, **kwargs)
            
    def __str__(self):
        return self.name


class mobile(models.Model):
    sId=models.IntegerField()
    phone=models.CharField(max_length=50)
class business_details(models.Model):
    category=models.CharField(max_length=100)
    bank_name=models.CharField(max_length=50)
    bsb=models.CharField(max_length=50)
    business_name=models.CharField(max_length=50)
    business_desc=models.CharField(max_length=200)
    business_address=models.CharField(max_length=200)
    email=models.EmailField(max_length=50)
    In=models.CharField(max_length=50)
    subcategory=models.CharField(max_length=50)
    Account_holder=models.CharField(max_length=50)
    account_number=models.CharField(max_length=50)
    business_contact=models.CharField(max_length=50)
    image1= models.ImageField(upload_to='images',blank= True,null=True)
    add_offer=models.CharField(max_length=50)

class category(models.Model):
    add_category=models.CharField(max_length=500)
class Meta:
    db_table = "django"
    model = mobile
    model = business_details
    
    fields = [
          'sId',
          'phone',
      ]
    
    fields = [
          
         'category',
         'bank_name',
          'bsb',
            'business_name',
            'business_desc',
            'business_address',
            'email',
            'In',
            'subcategory',
            'Account_holder',
            'account_number',
            'image1',
            'business_contact',
            'add_offer'
            
      ]
# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db import models

from authentication.utils import generate_ref_code
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        # my_recs = [p for p in qs if p.recommended_by == self.user]

        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        return my_recs

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)

# Create your models here.
