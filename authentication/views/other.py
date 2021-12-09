# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.http.request import HttpRequest
from requests.models import Response
import random
from serializers import UserSerializer, business_detailsSerializer,ProfileSerializer, categorySerializer, paymentSerializer,transSerializer
from ..models import business_details, category
from rest_framework import status
from django.http import response
from ..send_otp import send_otp
from django.shortcuts import render
import requests
import json
from rest_framework import generics
from rest_framework.views import APIView
from requests.auth import HTTPBasicAuth
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from ..forms import LoginForm, SignUpForm
from authentication.models import mobile
from authentication.models import business_details
from authentication.forms import MobileLoginForm, BusinessForm, categoryForm,paymentForm
from ..forms import business_detailsForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from geopy.distance import great_circle
from django.shortcuts import render, get_list_or_404
from django.views.generic import TemplateView, ListView
from django.db.models.functions import TruncMonth, TruncYear
from django.conf import settings

from ..models import *

from itertools import chain

from datetime import date

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from authentication.models import Transactions


# Create your views here.

def my_recommendations_view(request):
    user = request.user.is_authenticated
    profile = Profile.objects.filter(user=request.user)
    
    context = {'profile': profile}
    return render(request, 'profiles/main.html', context)
def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Profile.objects.get(id=profile_id)

            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Profile.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.save()
        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('main-view')
    context = {'form':form}
    return render(request, 'sign.html', context)

def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    print(request.session.get_expiry_age())
    return render(request, 'main.html', {})



@api_view(["GET"])
@csrf_exempt
def apis(request):
    url = 'https://discover.search.hereapi.com/v1/discover?at=52.5228,13.4124&q=679123&apiKey=vznif5oSnixasCz2y18sz9hYDTh41S8z82jmy07Tk1E'
    params = {'response': response}
    r = requests.get(url, params=params)
    books = r.json()

    return render(request, "business.html", books)


@api_view(["GET"])
@csrf_exempt
def trans(request):
    business_id = request.GET.get('business_id', None)
    if business_id is not None:
        business_payments = payments.objects.filter(
                business_id=business_id
            ).select_related('business').only(
                'id',
                'amount',
                'business_id',
                'business__business_name', 
            )
            
        details = []

        for payment in business_payments:
            details.append({
                'id': payment.id,
                'amount': payment.amount,
                'business_id': payment.business_id,
                'business_name':payment.business.business_name,
            })
        
        return JsonResponse(details, safe=False)   

    return JsonResponse({'error' : 'Bad request. Need `business_id`'}, status=400)     
@api_view(["GET"])
@csrf_exempt
def transact(request):    
    business_payments = payments.objects.all().select_related('business').only(
                'id',
                'amount',
                'business_id',
                'business__business_name', 
                'business__categories__name',
            )
            
    details = []

    for payment in business_payments:
            details.append({
                'id': payment.id,
                'amount': payment.amount,
                'business_id': payment.business_id,
                'business_name':payment.business.business_name,
                'categories':payment.business.categories.name,
            })
        
    return JsonResponse(details, safe=False)   

         
def index(request):
    try:
        users = User.objects.all()
        print(request.user)
        user = User.objects.get(username=request.user)
        return render(request, 'index.html', {'users': users, 'user': user})
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages from this view")


def transactions(request):
    transact=payments.objects.all()
    return render(request, 'transactions.html', {
         'transact': transact})
def shuffle(request):
    transact=Transactions.objects.all()
    transactions = Transactions.objects.filter().order_by('-price')

    count = len(transactions)
    total = 0
    shares = []
    factor = sum(range(count+1))
    
    for i, item in enumerate(transactions, start=1):
        total += int(item.price)
        shares.append({
            "sl": i,
            "order": count,
            "share": int(item.price),
            "id": item.id,
            "name": 'Customer',
            "to_give": 0,
            "multiplier": 0,
            "factor": factor,
        })
        count -= 1

    multiplier = (total * 0.5)/factor

    give_back = []
    for item in shares:
        item['to_give'] = item['order'] * multiplier
        item['multiplier'] = multiplier
        give_back.append(item)

   
    return render(request, 'shuffle.html', {
        'transact': transact,
        'give_back': give_back
    })


def business_list(request):
    movies = business_details.objects.all()
    cat = category.objects.all()
    return render(request, 'business_details.html',{"movies":movies,"cat":cat})


def paymentss(request):
    
    if request.method=="POST":
        form = paymentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/payment")
    else:
        form = paymentForm()
    return render(request,'payments.html',{"form":form})
    
def payment(request,id):
    payment = payments.objects.filter(business_id=id).first()
    
    users = Users.objects.all()

    # print (business.payments)
    
    return render(request, "payment.html", {
        "payment": payment,
        "users": users
    })
@api_view(["GET"])
@csrf_exempt
def business_pay(request,id):
    payment = payments.objects.filter(business_id=id)
    
    users = Users.objects.all()

    
    return JsonResponse({
        "payments" : paymentSerializer(payment,many=True).data,
         "users": UserSerializer(users,many=True).data,
    })
    
       
    
    
def notification(request):
    return render(request, 'notification.html')


def setting(request):
    return render(request, 'settings.html')


def pay(request):
    return render(request, 'pay.html')
def get_books(request):
    business_detail = request.user.id
    business_detail = business_details.objects.all()
    serializer = business_detailsSerializer(business_detail, many=True)
    return JsonResponse({'business_details': serializer.data}, safe=False, status=status.HTTP_200_OK)
@api_view(["GET"])
@csrf_exempt
def profile(request):
    profile = request.user.id
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return JsonResponse({'profile': serializer.data}, safe=False, status=status.HTTP_200_OK)
@api_view(["GET"])
@csrf_exempt
def show_category(request):
    cs = request.user.id
    cs = category.objects.all()
    serializer = categorySerializer(cs, many=True)
    return JsonResponse({'category': serializer.data}, safe=False, status=status.HTTP_200_OK)
@api_view(["GET"])
@csrf_exempt
def show_business(request):
    
    cs = business_details.objects.all()
    serializer =business_detailsSerializer(cs, many=True)
    return JsonResponse({"cs":serializer.data}, safe=False, status=status.HTTP_200_OK)

class paysection(APIView):
    serializer_class = paymentSerializer
    
    def post(self,request):
        Serializer = paymentSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return JsonResponse(Serializer.data)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def categories(request):
    cat = category.objects.all() 
    return render(request,'categories.html',{"cat":cat})


def Home(request):
    if request.method == "POST":
        categories_id= request.POST.get('categories_id')
        bank_name = request.POST.get('bank_name')
        bsb = request.POST.get('bsb')
        business_name = request.POST.get('business_name')
        business_desc = request.POST.get('business_desc')
        business_address = request.POST.get('business_address')
        email = request.POST.get('email')
        In = request.POST.get('In')
      
        business_code =request.POST.get('business_code')
        Account_holder = request.POST.get('Account_holder')
        account_number = request.POST.get('account_number')
        business_contact = request.POST.get('business_contact')
        image1 = request.FILES.get('image1')
        add_offer = request.POST.get('add_offer'),
        categories= category.objects.filter(id=categories_id).first()
        business_code =request.POST.get('business_code')
        business_code=categories.name[0:3] + business_name[0:3] +str(random.randint(100,200))
        obj = business_details(
            categories_id=categories_id,
            bank_name=bank_name,
            bsb=bsb,
            business_name=business_name,
            business_desc=business_desc,
            business_address=business_address,
            email=email,
            In=In,
            business_code=business_code.upper(),
            Account_holder=Account_holder,
            account_number=account_number,
            business_contact=business_contact,
            image1=image1,
            add_offer=add_offer,
        )
       
        obj.save()
    cat = category.objects.all() 
      
    return render(request,'business.html',{"cat":cat})
    
    
@api_view(["GET"]) 
def Categoryapi(request):
    categories=category.objects.all()
    serializer = categorySerializer(categories, many=True)
    return JsonResponse({"categories":serializer.data}, safe=False, status=status.HTTP_200_OK)

def Category(request):
    if request.method=="POST":
        form = categoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("categories/")
    else:
        form = categoryForm()
    return render(request,'category.html',{"form":form})
    

def percentage(part, whole):
    return 100 * float(part)/float(whole)

    print(percentage(5, 7))

    print('{:.2f}'.format(percentage(5, 7)))
    return render(request, "tables.html")

@api_view(["GET"])
def business(request):
    if request.GET.get('category_id',False):
        category_id= request.GET.get('category_id',False)
        movies=business_details.objects.filter(categories_id=category_id)
    else:
         movies=business_details.objects.all()

    serializer =  business_detailsSerializer(movies, many=True)
    return JsonResponse({"movies":serializer.data}, safe=False, status=status.HTTP_200_OK)

def tablelist(request):
    if request.GET.get('category_id',False):
        category_id= request.GET.get('category_id',False)
        movies=business_details.objects.filter(categories_id=category_id)
    else:

     movies = business_details.objects.all()
    codes = Transactions.objects.all()
    cat=category.objects.all()
    context = {"movie": movies,"cat":cat, "codes": codes, "host": 'http://13.232.49.240:8000'}
    

    return render(request, "tables.html", context)


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        form = SignUpForm()
    return render(request,'accounts/register.html',{"form":form})
def edit(request,id):
   
    business = get_object_or_404(business_details, pk=id)

    if request.method == 'POST':
        form = business_detailsForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business_details.html')
            # return redirect('/')
    else:
        form = business_detailsForm(instance = business)

    return render(request,'edit.html',{'form':form})
def update(request,id):
        cust = business_details.objects.get(id=id)
        cust.category = request.POST.get('category'),
        cust.bank_name = request.POST.get('bank_name'),
        cust.bsb = request.POST.get('bsb'),
        cust.business_name = request.POST.get('business_name'),
        cust.business_desc = request.POST.get('business_desc'),
        cust.business_address = request.POST.get('business_address'),
        cust.email = request.POST.get('email'),
        cust.In = request.POST.get('In'),
        cust.subcategory = request.POST.get('subcategory'),
        cust.Account_holder = request.POST.get('Account_holder'),
        cust.account_number = request.POST.get('account_number'),
        cust.business_contact = request.POST.get('business_contact'),
        cust.image1 = request.FILES.get('image1'),
        cust.add_offer = request.POST.get('add_offer')
        cust.save()
    
        return render(request, 'business_details.html')