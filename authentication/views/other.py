# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import re
from django.db.models.aggregates import Max
from django.http.request import HttpRequest
from requests.models import Response
import random
import string
from authentication.views.checkout import payment_cancel
from serializers import UserSerializer, business_detailsSerializer, businessSerializer, categorySerializer, \
    EmployeeSerializer, dealSerializer, paymentSerializer, rewardSerializer, transSerializer, usersSerializer
from ..models import business_details, category, roles, payments
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
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from ..forms import dealsForm, LoginForm, dealsForm, rewardsForm, rolesForm
from authentication.models import mobile
from authentication.models import business_details, Employee, payments
from authentication.forms import MobileLoginForm, BusinessForm, categoryForm, paymentForm
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
import geocoder
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
                'business_name': payment.business.business_name,
            })

        return JsonResponse(details, safe=False)

    return JsonResponse({'error': 'Bad request. Need `business_id`'}, status=400)


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
            'business': payment.business.business_name,
            'categories': payment.business.categories.name,
        })

    return JsonResponse(details, safe=False)


def index(request):
    
    return render(request, 'index.html')



def transactions(request):
    transact = payments.objects.all()
    return render(request, 'transactions.html', {
        'transact': transact})


def normaltransactions(request):
    transact = payments.objects.all()
    return render(request, 'normaltransactions.html', {
        'transact': transact})


def shuffle(request):
    transact = payments.objects.all()
    transactions = payments.objects.filter().order_by('amount').select_related('irich','user')

    count = len(transactions)
    total = 0
    shares = []
    factor = sum(range(count + 1))

    for i, item in enumerate(transactions, start=1):
        # print(item.amount)
        total += int(item.amount)/ int(item.irich.irich) / 10*int(item.irich.irich) 
        shares.append({
            "sl": i,
            "order": count,
            "share": int(item.amount)/10,
            "id": item.id,
            "username":item.user.username,
            "to_give": 0,
            "multiplier": 0,
            "factor": factor,
        })
        count -= 1

    count_sl = 1
    multiplier = (total * 0.5) / factor
    shares = sorted(shares, key=lambda i: i['share'], reverse=True)
    count_shares = len(shares)
    for dicts in shares:
        dicts['order'] = count_shares
        dicts['sl'] = count_sl
        count_shares = count_shares - 1
        count_sl += 1
    print(sorted(shares, key=lambda i: i['share'], reverse=True))
    
    give_back = []
    for item in shares:
        item['to_give'] = item['order'] * multiplier
        item['multiplier'] = multiplier
        give_back.append(item)
        # user=User.objects.get(username=item['username'])
        
        # wallets=wallet.objects.filter(user_id=user).update(earning=item['order'] * multiplier)
        # for i in wallets:
        #   i['earning'] = item['to_give']
          
        #   earning=item['order'] * multiplier
        #   wallets=wallet(earning=earning)
        #   wallets.save()

    return render(request, 'shuffle.html', {
        'transact': transact,
        'give_back': give_back
    })


def business_list(request):
    movies = business_details.objects.all()
    cat = category.objects.all()
    return render(request, 'business_details.html', {"movies": movies, "cat": cat})


def business_favourite(request, id):
    business = business_details.objects.all()
    cat = category.objects.all()
    payment = payments.objects.all()
    movies = payments.objects.filter(irich_id=id)
    return render(request, 'favourite.html', {"movies": movies, "cat": cat, "payment": payment})


@api_view(["GET"])
@csrf_exempt
def favourites(request):
    business_payments = payments.objects.all().select_related('irich').only(
        'id',

        'irich_id',
        'irich__business_name',
        'irich__categories__name',

        'irich__business_address'
    )

    details = []

    for payment in business_payments:
        details.append({
            'id': payment.id,
            # 'image1':payment.business.image1,
            'irich_id': payment.irich_id,
            'business_name': payment.irich.business_name,
            'categories': payment.irich.categories.name,
            'business_address': payment.irich.business_address,
        })

    return JsonResponse(details, safe=False)


def paymentss(request):
    id = request.POST.get('id')
    user = User.objects.filter(id=id)
    if request.method == "POST":
        form = paymentForm(request.POST)
        if form.is_valid():
            form.save(user)
            return HttpResponseRedirect("/home")
    else:
        form = paymentForm()
    return render(request, 'payments.html', {"form": form})


def normalpayment(request):
    Payment = payments.objects.all().select_related('irich', 'user').only('irich__business_name', 'irich__irich',
                                                                          'user__username')

    details = []
    # print (business.payments)
    for payment in Payment:
        details.append({
            'username': payment.user.username,
            'amount': payment.amount,
            'irich_percent': payment.irich.irich,
            'business_name': payment.irich.business_name,

        })
    return render(request, "normalpayments.html", {
        "details": details,
    })



def payment(request, id):
    payment = payments.objects.filter(business_id=id).first()

    users = User.objects.all()

    # print (business.payments)

    return render(request, "payment.html", {
        "payment": payment,
        "users": users
    })


def walletsection(request):
    wallet_user_ids = wallet.objects.all().values('user_id','irich_bonus')
    bonus=500
    print(wallet_user_ids)
    # wallet_user_ids.save()
    # print(wallet_user_ids)
    payment_vals = payments.objects.all()
    Payment = payments.objects.all().select_related('irich', 'user').only('irich__business_name', 'irich__irich',
                                                                       'user__username')
    print(payment_vals)
    # for i in result:
    #     print(i)
    details = []
    
    # print (business.payments)
    for payment in Payment:
        for dicts in wallet_user_ids:
            if dicts['user_id'] == payment.user_id:
               
                bonus = int(dicts['irich_bonus']) - 75
                from_value = wallet.objects.get(user_id=payment.user_id)
                from_value.irich_bonus = bonus
                # from_value.save()
                percentage=int(payment.irich.irich)
                details.append({
                    
                    'username': payment.user.username,
                    'amount': payment.amount,
                    'irich_percent': payment.irich.irich,
                    'initial_balance':int(bonus),
                    'business_name': payment.irich.business_name,
                    'net_amount':int(payment.amount)-percentage,
                    'bonus':int(bonus),
                })
        

    
    print(details)
    for dicts in wallet_user_ids:
            
                
            bonus = int(dicts['irich_bonus'])
                
    return render(request, "payments.html", {
        "details": details,
        "available_balance":int(bonus)
    })
@api_view(["GET"])
def walletsapi(request):
    transactions = payments.objects.filter().order_by('amount').select_related('irich', 'user')
    bonus=500
    count = len(transactions)
    total = 0
    shares = []
    factor = sum(range(count + 1))
     
    for i, item in enumerate(transactions, start=1):
        wallet_user_ids = wallet.objects.all().values('user_id','irich_bonus')
        Payment = payments.objects.all().select_related('irich', 'user').only('irich__business_name', 'irich__irich',
                                                                       'user__username')
        for dicts in wallet_user_ids:
            if dicts['user_id'] == item.user_id:
               
                bonus = int(dicts['irich_bonus']) - 75
                from_value = wallet.objects.get(user_id=item.user_id)
                from_value.irich_bonus = bonus
        # print(item.amount)
        total += int(item.amount)/ int(item.irich.irich) / 10*int(item.irich.irich) 
        shares.append({

            "order": count,
            "spent": int(item.amount),
            "username": item.user.username,
            # "share": int(item.amount),
            "earning": 0,
            # "multiplier": 0,
            # "factor": factor,
        })
        count -= 1

    multiplier = (total * 0.5) / factor

    give_back = []
    for item in shares:
        item['earning'] = item['order'] * multiplier
        item['multiplier'] = multiplier
        give_back.append(item)
    shares = sorted(shares, key=lambda i: i['spent'], reverse=True)
    # print(shares)
    shares_sort = sorted(shares, key=lambda i: i['earning'], reverse=True)
    # print(shares_sort)
    to_give = []
    spent = []

    for dicts in shares_sort:
        to_give.append(dicts['earning'])
    for dict in shares:
        spent.append(dict['spent'])
    # test_share = shares
    counter = 0
    for dict_share in shares:

        print(to_give[counter])

        dict_share['earning'] = to_give[counter]
        # dict_share['spent'] = spent[counter]
        counter += 1
    print(to_give)
    print(spent)
    print(shares)
    for dicts in wallet_user_ids:
            
                
            bonus = int(dicts['irich_bonus'])
    return JsonResponse({
        
        'give_back': give_back
    })


def wallets(request):
        transactions = payments.objects.filter().order_by('amount').select_related('irich', 'user')
        print(transactions)
        bonus=500
        
        
        user_id=request.POST.get('user_id')
        # print(user_id)
    
        # print(item.user_id)
        wallet_user_ids = wallet.objects.all().values('user_id','irich_bonus')
        # print(wallet_user_ids)
        Payment = payments.objects.all().select_related('irich', 'user').only('irich__business_name', 'irich__irich',
                                                                       'user__username')
        
        # print(item.amount)
        total = 0
        shares = []
        count = len(transactions)
        factor = sum(range(count + 1))
        for i, item in enumerate(transactions, start=1):
            
            total += int(item.amount)/ int(item.irich.irich) / 10*int(item.irich.irich) 
            shares.append({

                "order": count,
                "spent": int(item.amount)/10,
                "username": item.user.username,
                "share": int(item.amount),
                "to_give": 0,
                "multiplier": 0,
                "factor": factor,
            })
            
                    
            from_value = wallet.objects.get(user_id=user_id)
            from_value.irich_bonus = from_value.irich_bonus - 75
            count -= 1

        multiplier = (total * 0.5) / factor

        give_back = []
        for item in shares:
            item['to_give'] = item['order'] * multiplier
            item['multiplier'] = multiplier
            give_back.append(item)
        shares = sorted(shares, key=lambda i: i['spent'], reverse=True)
        # print(shares)
        shares_sort = sorted(shares, key=lambda i: i['to_give'], reverse=True)
    # print(shares_sort)
        to_give = []
        spent = []

        for dicts in shares_sort:
            to_give.append(dicts['to_give'])
        for dict in shares:
            spent.append(dict['spent'])
        # test_share = shares
        counter = 0
        for dict_share in shares:

            # print(to_give[counter])

            dict_share['to_give'] = to_give[counter]
            # dict_share['spent'] = spent[counter]
            counter += 1
        # print(to_give)
        # print(spent)
        # print(shares)
        for dicts in wallet_user_ids:
            
                
                bonus = int(dicts['irich_bonus'])
        return render(request, 'wallet.html', {
            # 'transact': transact,
            'give_back': give_back,
            "available_balance":int(bonus)
        })


@api_view(["GET"])
@csrf_exempt
def business_pay(request, id):
    payment = payments.objects.filter(irich_id=id)

    users = User.objects.all()

    return JsonResponse({
        "payments": paymentSerializer(payment, many=True).data,
        "users": UserSerializer(users, many=True).data,
    })


def notification(request):
    return render(request, 'notification.html')


def normaluser(request):
    paymentoption = payments.objects.all()
    return render(request, 'normalusers.html', {"paymentoption": paymentoption})
def showrewards(request):
    transact = payments.objects.all()
    transactions = payments.objects.filter().order_by('amount').select_related('irich')

    count = len(transactions)
    total = 0
    shares = []
    factor = sum(range(count + 1))

    for i, item in enumerate(transactions, start=1):
        # print(item.amount)
        total += int(item.amount)/ int(item.irich.irich) / 10*int(item.irich.irich) 
        shares.append({
            "sl": i,
            "order": count,
            "share": int(item.amount)/10,
            "id": item.id,

            "to_give": 0,
            "multiplier": 0,
            "factor": factor,
        })
        count -= 1

    count_sl = 1
    multiplier = (total * 0.125) / factor
    shares = sorted(shares, key=lambda i: i['share'], reverse=True)
    count_shares = len(shares)
    for dicts in shares:
        dicts['order'] = count_shares
        dicts['sl'] = count_sl
        count_shares = count_shares - 1
        count_sl += 1
    print(sorted(shares, key=lambda i: i['share'], reverse=True))

    give_back = []
    for item in shares:
        item['to_give'] = item['order'] * multiplier
        item['multiplier'] = multiplier
        give_back.append(item)

    return render(request, 'reward.html', {
        'transact': transact,
        'give_back': give_back
    })
# def wallets(request):
#     transactions = payments.objects.filter().order_by('amount').select_related('irich', 'user')
#     bonus=500
#     count = len(transactions)
#     total = 0
#     shares = []
#     factor = sum(range(count + 1))

#     for i, item in enumerate(transactions, start=1):
#         # print(item.amount)
#         total += int(item.amount)/ int(item.irich.irich) / 10*int(item.irich.irich) 
#         shares.append({

#             "order": count,
#             "share": int(item.amount)/10,
#             "id": item.id,
#             "username":item.user.username,
#             "to_give": 0,
#             "multiplier": 0,
#             "factor": factor,
#         })
#         count -= 1

#     count_sl = 1
#     multiplier = (total * 0.125) / factor
#     shares = sorted(shares, key=lambda i: i['share'], reverse=True)
#     count_shares = len(shares)
#     for dicts in shares:
#         dicts['order'] = count_shares
#         dicts['sl'] = count_sl
#         count_shares = count_shares - 1
#         count_sl += 1
#     print(sorted(shares, key=lambda i: i['share'], reverse=True))

#     give_back = []
#     for item in shares:
#         item['to_give'] = item['order'] * multiplier
#         item['multiplier'] = multiplier
#         give_back.append(item)

#     return render(request, 'wallet.html', {
       
#         'give_back': give_back,
#         "available_balance":int(bonus)
#     })

  


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
    serializer = business_detailsSerializer(cs, many=True)
    return JsonResponse({"cs": serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def rewardsapi(request):
    cs = rewards.objects.all()
    serializer = rewardSerializer(cs, many=True)
    return JsonResponse({"cs": serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def dealapi(request):
    cs = deals.objects.all()
    serializer = dealSerializer(cs, many=True)
    return JsonResponse({"cs": serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def show_users(request):
    employee = Employee.objects.all()
    users = User.objects.all()

    return JsonResponse({
        "employee": EmployeeSerializer(employee, many=True).data,
        "users": UserSerializer(users, many=True).data,
    })



class paysection(APIView):
    serializer_class = paymentSerializer
    
    def post(self, request):
        Serializer = paymentSerializer(data=request.data)
        data = request.data
        print(data)
        user_id = data.get("user")
        print(data.get("user"))
        wallet_user_ids = wallet.objects.all().values('user_id','irich_bonus')
        Payment = payments.objects.all().select_related('irich', 'user').only('irich__business_name', 'irich__irich',
                                                                      'user__username')
        for payment in Payment:

            for dicts in wallet_user_ids:
                if dicts['user_id'] == payment.user_id:
                    amount=request.POST.get('amount')
                    user=request.POST.get('user')
                    print(user)
                    bonus = int(dicts['irich_bonus']) - 75
                    from_value = wallet.objects.get(user_id=user_id)
                    from_value.irich_bonus = bonus
                    from_value.save()
        if Serializer.is_valid():
            Serializer.save()
            return JsonResponse(Serializer.data)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class adduser(APIView):

    serializer_class =UserSerializer
    
    def post(self, request):
        username=request.POST.get('username')
    
        
        Serializer=UserSerializer(data=request.data)
        if username is not None:
            # print(request.data)
            if Serializer.is_valid():
           
                
                
                 Serializer.save()
                 earning=0
                 irich_bonus=500
                 username=request.POST.get('username')
                 print(username)
                 user = User.objects.get(username=username)
                 phone=request.POST.get('phone')
                 print(phone)
                
                 
                 print(user.id)
                
                
                 ob=wallet(user_id=user.id,irich_bonus=irich_bonus,earning=earning)
            
            
                
                 ob.save()
                 return JsonResponse(Serializer.data)
        return JsonResponse(Serializer.errors)
           
 
class loginApi(APIView):
    serializer_class =usersSerializer
    def post(self, request):

        
        Serializer=usersSerializer(data=request.data)
        phone=request.POST.get('phone')
        # print(phone)
        # id=request.POST.get('id')
        role=roles.objects.get(designation='salesperson')
        # print(role.id)
        
        employee=Employee.objects.get(phone=phone)
        password=request.POST.get('password')
        user=User.objects.filter(password=password)
        print(password)
        # user=User.objects.get(id=employee.user_id)
        

        print(employee.designation_id)
        if role.id == employee.designation_id:
              return redirect('/BusinessAdd')
        elif role.id != employee.designation_id:
              return redirect('/mybusiness',{'phone' == phone})
            
       
           
        if Serializer.is_valid():
                
                
            
               return JsonResponse("error",safe=False) 
        return JsonResponse(Serializer.data)
        

       
      
        

def categories(request):
    cat = category.objects.all()
    return render(request, 'categories.html', {"cat": cat})


def normalcategories(request):
    cat = category.objects.all()
    return render(request, 'normalcategory.html', {"cat": cat})


def Home(request):
    if request.method == "POST":
        categories_id = request.POST.get('categories_id')
        bank_name = request.POST.get('bank_name')

        business_name = request.POST.get('business_name')
        business_desc = request.POST.get('business_desc')
        business_address = request.POST.get('business_address')
        email = request.POST.get('email')
        IFSC_code = request.POST.get('IFSC_code')
        irich = request.POST.get('irich')
        business_code = request.POST.get('business_code')
        Account_details = request.POST.get('Account_details')
        account_number = request.POST.get('account_number')
        business_contact = request.POST.get('business_contact')
        image1 = request.FILES.get('image1')
        subcategory = request.POST.get('subcategory')
        categories = category.objects.filter(id=categories_id).first()
        business_code = request.POST.get('business_code')
        # check = request.POST.get('lat')
        # business_code = categories.name[0:3] + business_name[0:3] + str(random.randint(100, 200))

        loc = str(business_address)
        print(loc)
        geolocator = Nominatim(user_agent="my_request")
        location = geolocator.geocode(loc)
        print(location)
        latitude = location.latitude
        # latitude = latitude[0]

        longitude = location.longitude
        # print(longitude)
        print(request.GET.get('check'))
        obj = business_details(
            categories_id=categories_id,
            bank_name=bank_name,
            IFSC_code=IFSC_code,
            business_name=business_name,
            business_desc=business_desc,
            business_address=business_address,
            email=email,
            subcategory=subcategory,
            Account_details=Account_details,
            business_code=business_code,
            irich=irich,
            account_number=account_number,
            business_contact=business_contact,
            image1=image1,


        )
        check = "true"
        print(check)
        # obj.save()
        cat = category.objects.all()
        return render(request, 'business_search.html', {"lat": latitude,
                                                        "long": longitude,
                                                        "categories_id": categories_id,
                                                        "bank_name": bank_name,
                                                        "business_name": business_name,
                                                        "IFSC_code": IFSC_code,
                                                        "business_desc":business_desc,
                                                        "business_address":business_address,
                                                        "email":email,
                                                        "subcategory":subcategory,
                                                        "Account_details":Account_details,
                                                        "business_code":business_code,
                                                        "irich":irich,
                                                        "account_number":account_number,
                                                        "business_contact":business_contact,
                                                        "image1":image1,
                                                         "cat":cat,

                                                     })

    
    cat = category.objects.all()
    return render(request, 'business.html',{"cat":cat})


def addsales(request):
    m = request.POST.get('username')
    det = User.objects.filter(username=m)
    if request.method == "POST":
        categories_id = request.POST.get('categories_id')
        bank_name = request.POST.get('bank_name')

        business_name = request.POST.get('business_name')
        business_desc = request.POST.get('business_desc')
        business_address = request.POST.get('business_address')
        email = request.POST.get('email')
        IFSC_code = request.POST.get('IFSC_code')
        irich = request.POST.get('irich')
        business_code = request.POST.get('business_code')
        Account_details = request.POST.get('Account_details')
        account_number = request.POST.get('account_number')
        business_contact = request.POST.get('business_contact')
        image1 = request.FILES.get('image1')

        categories = category.objects.filter(id=categories_id).first()
        business_code = request.POST.get('business_code')
        business_code = categories.name[0:3] + business_name[0:3] + str(random.randint(100, 200))
        # obj = business_details(
        #     categories_id=categories_id,
        #     bank_name=bank_name,
        #     IFSC_code=IFSC_code,
        #     business_name=business_name,
        #     business_desc=business_desc,
        #     business_address=business_address,
        #     email=email,
        #     Account_details=Account_details,
        #     business_code=business_code.upper(),
        #     irich=irich,
        #     account_number=account_number,
        #     business_contact=business_contact,
        #     image1=image1,
        #
        # )
        #
        # obj.save()
    cat = category.objects.all()

    return render(request, 'salesperson.html', {"cat": cat, "det": det})


@api_view(["GET"])
def Categoryapi(request):
    categories = category.objects.all()
    serializer = categorySerializer(categories, many=True)
    return JsonResponse({"categories": serializer.data}, safe=False, status=status.HTTP_200_OK)


def Category(request):
    if request.method == "POST":
        form = categoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/category")
    else:
        form = categoryForm()
    return render(request, 'category.html', {"form": form})


def role(request):
    if request.method == "POST":
        form = rolesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/showrole")
    else:
        form = rolesForm()
    return render(request, 'roles.html', {"form": form})


def rewardcreation(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        targeted_amount = request.POST.get('targeted_amount')
        referral_member = request.POST.get('referral_member')

        obj = rewards(
            start_date=start_date,
            end_date=end_date,
            targeted_amount=targeted_amount,
            referral_member=referral_member,

        )

        obj.save()
    return render(request, 'rewards.html')


def showrole(request):
    roleshow = roles.objects.all()
    return render(request, 'role.html', {"roleshow": roleshow})


def createdeal(request):
    if request.method == "POST":
        title=request.POST.get('title')
        description=request.POST.get('description')

        obj = deals(title=title,
        description=description
           
        )

        obj.save()
    
    return render(request, 'createdeal.html')


def showdeal(request):
    dealshow = deals.objects.all()
    return render(request, 'deals.html', {"dealshow": dealshow})


# def percentage(part, whole):
#     return 100 * float(part)/float(whole)

#     print(percentage(5, 7))

#     print('{:.2f}'.format(percentage(5, 7)))
#     return render(request, "tables.html")

@api_view(["GET"])
def business(request):
    if request.GET.get('category_id', False):
        category_id = request.GET.get('category_id', False)
        movies = business_details.objects.filter(categories_id=category_id)
    else:
        movies = business_details.objects.all()

    serializer = business_detailsSerializer(movies, many=True)
    return JsonResponse({"movies": serializer.data}, safe=False, status=status.HTTP_200_OK)
@api_view(["GET"])
def mybusiness(request):
    phone=request.POST.get('phone')
    print(phone)
    # if user == 'business owner':
    
    user=User.objects.get(username="business owner")
    business=business_details.objects.filter(user=user.id)
    # if user == '1':
    #     businesslist=business_details.objects.filter(user=user)
        
    serializer = business_detailsSerializer(business, many=True)
    usernames=serializer.data
    list_usernames = []
    for name in usernames:
        if name['user'] == user.id:
          username = name['user']
          print(username)  
    return JsonResponse({"business":serializer.data}, safe=False)


def tablelist(request):
    if request.GET.get('category_id', False):
        category_id = request.GET.get('category_id', False)
        movies = business_details.objects.filter(categories_id=category_id)
    else:

        movies = business_details.objects.all()
    codes = Transactions.objects.all()
    cat = category.objects.all()
    context = {"movie": movies, "cat": cat, "codes": codes, "host": 'http://13.232.49.240:8000'}

    return render(request, "tables.html", context)
def saleslist(request):
    if request.GET.get('category_id', False):
        category_id = request.GET.get('category_id', False)
        movies = business_details.objects.filter(categories_id=category_id)
    else:

        movies = business_details.objects.all()
    codes = Transactions.objects.all()
    cat = category.objects.all()
    context = {"movie": movies, "cat": cat, "codes": codes, "host": 'http://13.232.49.240:8000'}

    return render(request, "saleslist.html", context)
def normallist(request):
    if request.GET.get('category_id', False):
        category_id = request.GET.get('category_id', False)
        movies = business_details.objects.filter(categories_id=category_id)
    else:

        movies = business_details.objects.all()
    codes = Transactions.objects.all()
    cat = category.objects.all()
    context = {"movie": movies, "cat": cat, "codes": codes, "host": 'http://13.232.49.240:8000'}

    return render(request, "normallist.html", context)


def businesslist(request):
    print('hiiii')
    user=request.POST.get('user')
    # user_id=request.POST.get('user_id')
    print(user)
    
    movies = business_details.objects.all()
    print(movies)
    details = []
    # print (business.payments)
    for movie in movies:
        details.append({
            'business_name': movie.business_name,
            'name': movie.categories.name,
            'business_desc': movie.business_desc,
            'business_address': movie.business_address,
            'email': movie.email,
            'Account_details': movie.Account_details,
            'account_number': movie.account_number,
            'business_contact': movie.business_contact,

        })
    return render(request, "businesslist.html", {
        "details": details,
    })


def signin(request):
    try:
        m = request.POST['username']
        p = request.POST['password']
        user=request.user
        print(user)
        if m and p:
            det = User.objects.get(username=m)
            if det.is_superuser == True:
                
                if det.password == p:
                    request.session['name'] = det.username
                    return redirect('/categories')
                

            elif det.is_staff == True:

                request.session['name'] = "salesperson"
                return redirect('/addsales')
            elif m == "business owner":
                username=request.POST.get('username')
                print(m)
                request.session['name'] = "business owner"
                movies = business_details.objects.all()
                print(movies)
                details = []
            # print (business.payments)
            for movie in movies:
                details.append({
                    'business_name': movie.business_name,
                    'name': movie.categories.name,
                    'business_desc': movie.business_desc,
                    'business_address': movie.business_address,
                    'email': movie.email,
                    'Account_details': movie.Account_details,
                    'account_number': movie.account_number,
                    'business_contact': movie.business_contact,

                })
                return render(request,'businesslist.html',{"m":m,"details":details})

            else:
                request.session['name'] = "username"
                return normaluser(request)
        return render(request, 'accounts/login.html', {'error': "please check the password", "m": m})
    except:
        return render(request, 'accounts/login.html', {'error': "please check the password"})


def logout(request):
    try:
        del request.session['name']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


def users(request):
    employee = Employee.objects.select_related('user', 'designation', 'business').all()

    return render(request, "users.html", {"employee": employee})


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        is_staff = 1
        is_active = 1
        is_superuser = False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        earning=0
        irich_bonus=500
        date_joined = datetime.date.today()
        user = User.objects.create(
            username=username,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            date_joined=date_joined
        )
        N = 8
        phone = request.POST.get('phone')
        referral_code = request.POST.get('referral_code')
        postcode = request.POST.get('postcode')

        referral = ''.join(random.choices(string.ascii_uppercase +
                                          string.digits, k=N))

        obj = Employee(
            user_id=user.id,
            phone=phone,
            referral_code=referral_code,
            postcode=postcode,
            referral=referral,
            
        )
        ob=wallet(user_id=user.id,irich_bonus=irich_bonus,earning=earning)
        
        
        obj.save()
        ob.save()
    object=Employee.objects.all()
    return render(request, 'accounts/register.html',{'object':object})
def bonus(request):
    user_id=request.POST.get('user_id')
    movies = wallet.objects.filter(user_id=user_id).first()

    details = []
    # print (business.payments)
    for movie in movies:
        details.append({
            'irich_bonus':movie.irich_bonus

        })

        
        
    
    
    return render(request, 'wallet.html',{"details":details})

def edit(request, id):
    object = business_details.objects.get(id=id)
    return render(request, 'edit.html', {'object': object})


def useredit(request, id):
    object = Employee.objects.get(id=id)
    return render(request, 'useredit.html', {'object': object})


def edit_user_role(request, id):
    user_roles = roles.objects.all()
    user = User.objects.get(id=id)

    if request.method == "POST":
        designation_id = request.POST.get('role')

        employee = Employee.objects.filter(user_id=id).first()
        if employee is None:
            employee = Employee.objects.create(
                designation_id=designation_id,
                user_id=id
            )
        else:
            employee.designation_id = designation_id
            employee.save()

    else:
        employee = Employee.objects.filter(user_id=id).first()

    return render(request, 'edit-role.html', {
        'roles': user_roles,
        'user': user,
        'role_id': employee.designation_id if employee is not None else ''
    })


def edit_business(request, id):
    business_edit = business_details.objects.all()
    user = User.objects.get(id=id)

    if request.method == "POST":
        business_id = request.POST.get('business_name')

        employee = Employee.objects.filter(user_id=id).first()
        if employee is None:
            employee = business_details.objects.create(
                business_id=business_id,
                user_id=id
            )
        else:
            employee.business_id = business_id
            employee.save()

    else:
        employee = Employee.objects.filter(user_id=id).first()

    return render(request, 'business-edit.html', {
        'business_edit': business_edit,
        'user': user,
        'business_id': employee.business_id if employee is not None else ''
    })


def categoryedit(request, id):
    object = category.objects.get(id=id)
    return render(request, 'categoryedit.html', {'object': object})


def roledit(request, id):
    object = roles.objects.get(id=id)
    return render(request, 'roleedit.html', {'object': object})


def dealedit(request, id):
    object = deals.objects.get(id=id)
    return render(request, 'dealedit.html', {'object': object})


def userupdate(request, id):
    object = User.objects.get(id=id)
    form = UserCreationForm(request.POST, instance=object)
    if form.is_valid:
        form.save()
        object = Employee.objects.all()
        return redirect('/users')


def update(request, id):
    object = business_details.objects.get(id=id)
    form = business_detailsForm(request.POST, instance=object)
    if form.is_valid:
        form.save()
        object = business_details.objects.all()
        return redirect('/categories')


def businessupdate(id):
    object = business_details.objects.get(id=id)

    return redirect('/businesslist', {'object': object})


def categoryupdate(request, id):
    object = category.objects.get(id=id)
    form = categoryForm(request.POST, instance=object)
    if form.is_valid:
        form.save()
        object = category.objects.all()
        return redirect('/categories')


def roleupdate(request, id):
    object = roles.objects.get(id=id)
    form = rolesForm(request.POST, instance=object)
    if form.is_valid:
        form.save()
        object = roles.objects.all()
        return redirect('/showrole')


def dealupdate(request, id):
    object = deals.objects.get(id=id)
    form = dealsForm(request.POST, instance=object)
    if form.is_valid:
        form.save()
        object = deals.objects.all()
        return redirect('/deals')


def delete(request, id):
    business_details.objects.filter(id=id).delete()
    return redirect('/categories')


def userdelete(request, id):
    Employee.objects.filter(id=id).delete()
    return redirect('/users')


def categorydelete(request, id):
    category.objects.filter(id=id).delete()
    return redirect('/categories')


def roledelete(request, id):
    roles.objects.filter(id=id).delete()
    return redirect('/showrole')


def dealdelete(request, id):
    deals.objects.filter(id=id).delete()
    return redirect('/deals')


class BusinessAddApi(APIView):
    serializer_class = businessSerializer

    def post(self, request):
        Serializer = businessSerializer(data=request.data)

        categoryobject = category.objects.all().only('name')
        if Serializer.is_valid():
            categories = request.POST.get('categories')
            bank_name = request.POST.get('bank_name')
            business_name = request.POST.get('business_name')
            business_desc = request.POST.get('business_desc')
            business_address = request.POST.get('business_address')
            loc = str(business_address)
            print(loc)
            geolocator = Nominatim(user_agent="my_request")
            location = geolocator.geocode(loc)
            print(location)
            latitude = location.latitude
            # latitude = latitude[0]

            longitude = location.longitude
            email = request.POST.get('email')
            IFSC_code = request.POST.get('IFSC_code')
            irich = request.POST.get('irich')
            business_code = request.POST.get('business_code')
            Account_details = request.POST.get('Account_details')
            account_number = request.POST.get('account_number')
            business_contact = request.POST.get('business_contact')
            image1 = request.FILES.get('image1')
            subcategory = request.POST.get('subcategory')
            # categories = category.objects.filter(id=categories_id).first()
            print(categories)
            business_code = request.POST.get('business_code')
            # check = request.POST.get('lat')
            business_code =  business_name[0:3] + str(random.randint(100, 200))


            obj = business_details(
                categories_id=categories,
                bank_name=bank_name,
                IFSC_code=IFSC_code,
                business_name=business_name,
                business_desc=business_desc,
                business_address=business_address,
                email=email,
                subcategory=subcategory,
                Account_details=Account_details,
                business_code=business_code,
                irich=irich,
                account_number=account_number,
                business_contact=business_contact,
                image1=image1,
                latitude=latitude,
                longitude=longitude,

            )
            
            obj.save()
        
        return JsonResponse(Serializer.data)


def search_map(request):
    print('hiii')
    if request.method == "POST":
        categories_id = request.POST.get('categories_id')
        bank_name = request.POST.get('bank_name')
        business_name = request.POST.get('business_name')
        business_desc = request.POST.get('business_desc')
        business_address = request.POST.get('business_address')
        loc = str(business_address)
        print(loc)
        geolocator = Nominatim(user_agent="my_request")
        location = geolocator.geocode(loc)
        print(location)
        latitude = location.latitude
        # latitude = latitude[0]

        longitude = location.longitude
        email = request.POST.get('email')
        IFSC_code = request.POST.get('IFSC_code')
        irich = request.POST.get('irich')
        business_code = request.POST.get('business_code')
        Account_details = request.POST.get('Account_details')
        account_number = request.POST.get('account_number')
        business_contact = request.POST.get('business_contact')
        image1 = request.FILES.get('image1')
        subcategory = request.POST.get('subcategory')
        categories = category.objects.filter(id=categories_id).first()
        print(categories)
        business_code = request.POST.get('business_code')
        # check = request.POST.get('lat')
        business_code =  business_name[0:3] + str(random.randint(100, 200))


        obj = business_details(
            categories_id=categories_id,
            bank_name=bank_name,
            IFSC_code=IFSC_code,
            business_name=business_name,
            business_desc=business_desc,
            business_address=business_address,
            email=email,
            subcategory=subcategory,
            Account_details=Account_details,
            business_code=business_code,
            irich=irich,
            account_number=account_number,
            business_contact=business_contact,
            image1=image1,
            latitude=latitude,
            longitude=longitude,

        )
        check = "true"
        print(check)
        obj.save()
    cat=category.objects.all()
    return render(request, 'business.html',{"cat":cat} )
