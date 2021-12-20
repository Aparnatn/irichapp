# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.http.request import HttpRequest
from requests.models import Response
import random
from authentication.views.checkout import payment_cancel
from serializers import UserSerializer, business_detailsSerializer, categorySerializer,EmployeeSerializer,paymentSerializer,transSerializer
from ..models import business_details, category,roles,payments
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
from ..forms import LoginForm, rolesForm
from authentication.models import mobile
from authentication.models import business_details,Employee,payments
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
                'business':payment.business.business_name,
                'categories':payment.business.categories.name,
            })
        
    return JsonResponse(details, safe=False)   

         
def index(request):
    # try:
    #     users = User.objects.all()
    #     print(request.user)
    #     user = User.objects.get(username=request.user)
        return render(request, 'index.html')
    # except Exception as e:
    #     print(e)
    #     return HttpResponse("Please login from admin site for sending messages from this view")


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
def business_favourite(request,id):
    business = business_details.objects.all()
    cat = category.objects.all()
    payment = payments.objects.all()
    movies = payments.objects.filter(business_id=id)
    return render(request, 'favourite.html',{"movies":movies,"cat":cat,"payment":payment})

def paymentss(request):
    
    if request.method=="POST":
        form = paymentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/home")
    else:
        form = paymentForm()
    return render(request,'payments.html',{"form":form})
    
def payment(request,id):
    payment = payments.objects.filter(business_id=id).first()
    
    users = User.objects.all()

    # print (business.payments)
    
    return render(request, "payment.html", {
        "payment": payment,
        "users": users
    })
@api_view(["GET"])
@csrf_exempt
def business_pay(request,id):
    payment = payments.objects.filter(business_id=id)
    
    users = User.objects.all()

    
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
@api_view(["GET"])
@csrf_exempt
def show_users(request):
    employee=Employee.objects.all()
    users = User.objects.all()
    
    return JsonResponse({
        "employee" : EmployeeSerializer(employee,many=True).data,
         "users": UserSerializer(users,many=True).data,
    })
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
       
        business_name = request.POST.get('business_name')
        business_desc = request.POST.get('business_desc')
        business_address = request.POST.get('business_address')
        email = request.POST.get('email')
        IFSC_code = request.POST.get('IFSC_code')
        irich=request.POST.get('irich')
        business_code =request.POST.get('business_code')
        Account_details=request.POST.get('Account_details')
        account_number = request.POST.get('account_number')
        business_contact = request.POST.get('business_contact')
        image1 = request.FILES.get('image1')
        
        categories= category.objects.filter(id=categories_id).first()
        business_code =request.POST.get('business_code')
        business_code=categories.name[0:3] + business_name[0:3] +str(random.randint(100,200))
        obj = business_details(
            categories_id=categories_id,
            bank_name=bank_name,
            IFSC_code=IFSC_code,
            business_name=business_name,
            business_desc=business_desc,
            business_address=business_address,
            email=email,
            Account_details=Account_details,
            business_code=business_code.upper(),
            irich=irich,
            account_number=account_number,
            business_contact=business_contact,
            image1=image1,
            
        )
       
        obj.save()
    cat = category.objects.all() 
      
    return render(request,'business.html',{"cat":cat})
    
def addsales(request):
    m=request.POST.get('username')
    det=User.objects.filter(username=m)
    if request.method == "POST":
        categories_id= request.POST.get('categories_id')
        bank_name = request.POST.get('bank_name')
       
        business_name = request.POST.get('business_name')
        business_desc = request.POST.get('business_desc')
        business_address = request.POST.get('business_address')
        email = request.POST.get('email')
        IFSC_code = request.POST.get('IFSC_code')
        irich=request.POST.get('irich')
        business_code =request.POST.get('business_code')
        Account_details=request.POST.get('Account_details')
        account_number = request.POST.get('account_number')
        business_contact = request.POST.get('business_contact')
        image1 = request.FILES.get('image1')
        
        categories= category.objects.filter(id=categories_id).first()
        business_code =request.POST.get('business_code')
        business_code=categories.name[0:3] + business_name[0:3] +str(random.randint(100,200))
        obj = business_details(
            categories_id=categories_id,
            bank_name=bank_name,
            IFSC_code=IFSC_code,
            business_name=business_name,
            business_desc=business_desc,
            business_address=business_address,
            email=email,
            Account_details=Account_details,
            business_code=business_code.upper(),
            irich=irich,
            account_number=account_number,
            business_contact=business_contact,
            image1=image1,
            
        )
       
        obj.save()
    cat = category.objects.all() 
      
    return render(request,'salesperson.html',{"cat":cat,"det":det})   
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
            return HttpResponseRedirect("/category")
    else:
        form = categoryForm()
    return render(request,'category.html',{"form":form})
def role(request):
    if request.method=="POST":
        form = rolesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/showrole")
    else:
        form = rolesForm()
    return render(request,'roles.html',{"form":form})   
def showrole(request):
    roleshow=roles.objects.all()
    return render(request,'role.html',{"roleshow":roleshow})

# def percentage(part, whole):
#     return 100 * float(part)/float(whole)

#     print(percentage(5, 7))

#     print('{:.2f}'.format(percentage(5, 7)))
#     return render(request, "tables.html")

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


def signin(request):
   try:
    m=request.POST['username']
    p=request.POST['password']
    if m and p:
       
        if m=="superadmin":
            det=User.objects.get(username=m)
            if det.password==p:
                request.session['name']=det.username
                return business_list(request)
       
        elif m=="salesperson":
           
                request.session['name']="salesperson"
                return redirect('/addsales')
       
        else:
            request.session['name']="username"
            return  notification(request)
    return render(request,'accounts/login.html',{'error':"please check the password","m": m})
   except:
          return render(request,'accounts/login.html',{'error':"please check the password"})
def logout(request):
    try:
        del request.session['name']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")
def users(request):
    user=User.objects.all()
    employee=Employee.objects.all()
    role=roles.objects.all()
    
    return render(request,"users.html",{"user":user,"employee":employee,"role":role})
# def adduser(request,id):
   
#     return render(request,"users.html",{"users":users})
def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        is_staff = 1
        is_active = 1
        is_superuser = False
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        date_joined= datetime.date.today()
        user = User.objects.create(
            username = username,
            is_staff = is_staff,
            is_active =is_active,
            is_superuser = is_superuser,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            date_joined=date_joined
        )
    
        phone = request.POST.get('phone')
        referral_code = request.POST.get('referral_code')
        postcode = request.POST.get('postcode')
        designation=request.POST.get('designation')
        referral=random.randint(100,200)
       
        obj=Employee(
            user_id=user.id,
            phone = phone,
            referral_code = referral_code,
            postcode = postcode,   
            referral=referral,
        )
        obj.save()

      
    return render(request,'accounts/register.html')
    
def edit(request,id):
   
    object=business_details.objects.get(id=id)
    return render(request,'edit.html',{'object':object})
def useredit(request,id):
   
    object=Employee.objects.get(id=id)
    return render(request,'useredit.html',{'object':object})
def adduser(request,id):
    role=roles.objects.all()
    object=User.objects.get(id=id)
    
        
    
    return render(request,'adduser.html',{'role':role,'object':object})
def adduserslist(request):
    role=roles.objects.all()
    
    if request.method == "POST":
        designation_id=request.POST.get('designation_id')
        
        designation=roles.objects.filter(designation=designation_id)
        user = Employee(designation_id=designation_id)
        user.save()
     
    return render(request,'adduser.html',{'role':role})
def categoryedit(request,id):
   
    object=category.objects.get(id=id)
    return render(request,'categoryedit.html',{'object':object})
def roledit(request,id):
   
    object=roles.objects.get(id=id)
    return render(request,'roleedit.html',{'object':object})
def userupdate(request,id):
       object=User.objects.get(id=id)
       form=UserCreationForm(request.POST,instance=object)
       if form.is_valid:
        form.save()
        object=Employee.objects.all()
        return redirect('/users')
    
def update(request,id):
       object=business_details.objects.get(id=id)
       form=business_detailsForm(request.POST,instance=object)
       if form.is_valid:
        form.save()
        object=business_details.objects.all()
        return redirect('/categories')
def categoryupdate(request,id):
       object=category.objects.get(id=id)
       form=categoryForm(request.POST,instance=object)
       if form.is_valid:
        form.save()
        object=category.objects.all()
        return redirect('/categories')
def roleupdate(request,id):
       object=roles.objects.get(id=id)
       form=rolesForm(request.POST,instance=object)
       if form.is_valid:
        form.save()
        object=roles.objects.all()
        return redirect('/showrole')
def delete(request,id):   
        business_details.objects.filter(id=id).delete()
        return redirect('/categories')
def userdelete(request,id):   
        Employee.objects.filter(id=id).delete()
        return redirect('/users')
def categorydelete(request,id):   
        category.objects.filter(id=id).delete()
        return redirect('/categories')
def roledelete(request,id):   
        roles.objects.filter(id=id).delete()
        return redirect('/showrole')