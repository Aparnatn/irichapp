# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.http.request import HttpRequest
from serializers import business_detailsSerializer,ProfileSerializer, categorySerializer,transSerializer
from ..models import business_details, category
from rest_framework import status
from django.http import response
from ..send_otp import send_otp
from django.shortcuts import render
import requests
import json
from qr_code.qrcode.utils import QRCodeOptions

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
from authentication.forms import MobileLoginForm, BusinessForm, categoryForm
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



# def qr(request):
#     currency = 'INR'
#     amount = 20000  # Rs. 200

#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))

#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'

#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url

#     return render(request, 'index.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
# @csrf_exempt
# def paymenthandler(request):

#     # only accept POST request.
#     if request.method == "POST":
#         try:

#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             if result is None:
#                 amount = 20000  # Rs. 200
#                 try:

#                     # capture the payemt
#                     razorpay_client.payment.capture(payment_id, amount)

#                     # render success page on successful caputre of payment
#                     return render(request, 'paymentsuccess.html')
#                 except:

#                     # if there is an error while capturing payment.
#                     return render(request, 'paymentfail.html')
#             else:

#                 # if signature verification fails.
#                 return render(request, 'paymentfail.html')
#         except:

#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()


class HomepageView(TemplateView):
    template_name = 'api.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        bills = Bill.my_query.get_queryset().unpaid()[:10]
        payrolls = Payroll.my_query.get_queryset().unpaid()[:10]
        expenses = GenericExpense.my_query.get_queryset().unpaid()[:10]
        context.update({'bills': bills,
                        'payroll': payrolls,
                        'expenses': expenses
                        })
        return context


class BillListView(ListView):
    model = Bill
    template_name = 'page_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = Bill.objects.all()
        queryset = Bill.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)
        page_title = 'Bills List'
        categories = BillCategory.objects.all()
        search_name, cate_name, paid_name = [self.request.GET.get('search_name', None),
                                             self.request.GET.getlist(
                                                 'cate_name', None),
                                             self.request.GET.getlist(
                                                 'paid_name', None)
                                             ]
        total_value, paid_value, diff, category_analysis = Bill.analysis(
            self.object_list)
        currency = CURRENCY
        context.update(locals())
        return context


class PayrollListView(ListView):
    model = Payroll
    template_name = 'page_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = Payroll.objects.all()
        queryset = Payroll.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PayrollListView, self).get_context_data(**kwargs)
        page_title = 'Payroll List'
        categories = PayrollCategory.objects.all()
        persons = Person.objects.all()
        search_name, cate_name, paid_name, person_name = [self.request.GET.get('search_name', None),
                                                          self.request.GET.getlist(
                                                              'cate_name', None),
                                                          self.request.GET.getlist(
                                                              'paid_name', None),
                                                          self.request.GET.getlist(
                                                              'person_name', None)
                                                          ]
        total_value, paid_value, diff, category_analysis = Payroll.analysis(
            self.object_list)
        currency = CURRENCY
        context.update(locals())
        return context


class ExpensesListView(ListView):
    model = GenericExpense
    template_name = 'page_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = GenericExpense.objects.all()
        queryset = GenericExpense.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ExpensesListView, self).get_context_data(**kwargs)
        page_title = 'Expenses List'
        categories = GenericExpenseCategory.objects.all()
        search_name, cate_name, paid_name = [self.request.GET.get('search_name', None),
                                             self.request.GET.getlist(
                                                 'cate_name', None),
                                             self.request.GET.getlist(
                                                 'paid_name')
                                             ]
        total_value, paid_value, diff, category_analysis = GenericExpense.analysis(
            self.object_list)
        currency = CURRENCY
        context.update(locals())
        return context


def report_view(request):
    startDate = request.GET.get('startDate', '2018-01-01')
    endDate = request.GET.get('endDate', '2018-12-31')
    if startDate > endDate:
        startDate, endDate = '2018-01-01', '2018-12-31'
    date_start = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()
    date_end = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()
    bills = Bill.my_query.get_queryset().filter_by_date(date_start, date_end)
    payrolls = Payroll.my_query.get_queryset().filter_by_date(date_start, date_end)
    expenses = GenericExpense.my_query.get_queryset().filter_by_date(date_start, date_end)
    queryset = sorted(chain(bills, payrolls, expenses),
                      key=lambda instance: instance.date_expired
                      )
    bill_total_value, bill_paid_value, bill_diff, bill_category_analysis = DefaultExpenseModel.analysis(
        bills)
    payroll_total_value, payroll_paid_value, payroll_diff, bill_category_analysis = DefaultExpenseModel.analysis(
        payrolls)
    expense_total_value, expense_paid_value, expense_diff, expense_category_analysis = DefaultExpenseModel.analysis(
        expenses)

    bill_by_month, payroll_by_month, expenses_by_month, totals_by_month = [], [], [], []
    months_list = []
    while date_start < date_end:
        months_list.append(date_start)

    for date in months_list:
        start = date.replace(day=1)
        next_month = date.replace(day=28) + datetime.timedelta(days=4)
        days = int(str(next_month).split('-')[-1])
        end = next_month - datetime.timedelta(days=days)
        print(next_month, end)
        this_month_bill_queryset = bills.filter(
            date_expired__range=[start, end])
        this_month_bills = DefaultExpenseModel.analysis(
            this_month_bill_queryset)
        this_month_payroll_queryset = payrolls.filter(
            date_expired__range=[start, end])
        this_month_payroll = DefaultExpenseModel.analysis(
            this_month_payroll_queryset)
        this_month_expense_queryset = expenses.filter(
            date_expired__range=[start, end])
        this_month_expense = DefaultExpenseModel.analysis(
            this_month_expense_queryset)
        bill_by_month.append(this_month_bills)
        payroll_by_month.append(this_month_expense)
        expenses_by_month.append(this_month_payroll)
        totals_by_month.append([this_month_bills[0]+this_month_expense[0] + this_month_payroll[0],
                                this_month_bills[1] + this_month_expense[1] +
                                this_month_payroll[1],
                                this_month_bills[2] +
                                this_month_expense[2] + this_month_payroll[2]
                                ])

    totals = [payroll_total_value + bill_total_value + expense_total_value,
              bill_paid_value + payroll_paid_value + expense_paid_value,
              bill_diff + payroll_diff + expense_diff
              ]
    currency = CURRENCY
    context = locals()
    return render(request, 'report.html', context=context)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def welcome(request):
    content = {"message": "Welcome to the BookStore!"}
    return JsonResponse(content)


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
# Create your views here.
def trans(request):
    transact=Transactions.objects.all()
    serializer = transSerializer(transact, many=True)
    return JsonResponse({'transact': serializer.data}, safe=False, status=status.HTTP_200_OK)
   


# Create your views here.


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
            "name": "customer_{item.id}",
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

   
    return render(request, 'transactions.html', {
        'transact': transact,
        'give_back': give_back
    })
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
    return render(request, 'business_details.html')


def payment(request):
    transact=Transactions.objects.all()
    item=Transactions.objects.filter(price='price')
    a= (200*15/100)
    b =a
    return render(request, 'payment.html',{'transact':transact,'b':b})
    
    
def notification(request):
    return render(request, 'notification.html')


def setting(request):
    return render(request, 'settings.html')


def pay(request):
    return render(request, 'pay.html')


def api(request):
    restraunt_objs = Restraunt.objects.all()

    pincode = request.GET.get('pincode')
    km = request.GET.get('km')
    user_lat = None
    user_long = None

    if pincode:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(int(pincode))
        user_lat = location.latitude
        user_long = location.longitude

    payload = []
    for restraunt_obj in restraunt_objs:
        result = {}
        result['name'] = restraunt_obj.name
        result['image'] = restraunt_obj.image
        result['description'] = restraunt_obj.description
        result['pincode'] = restraunt_obj.pincode
        if pincode:
            first = (float(user_lat), float(user_long))
            second = (float(restraunt_obj.lat), float(restraunt_obj.lon))
            result['distance'] = int(great_circle(first, second).miles)

        payload.append(result)

        if km:
            if result['distance'] > int(km):
                payload.pop()

    return JsonResponse(payload, safe=False)


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


def categories(request):
    if request.method == "POST":
        cs = categoryForm(request.POST, request.FILES)

        if cs.is_valid():
            cs.save()
            messages.success(request, ('Your movie was successfully added!'))
        else:
            messages.error(request, 'Error saving form')
            return redirect("category")
    cs = categoryForm()
    # movies = business_details.objects.all()
    context = {"cs": cs}
    return render(request, "category.html", context)


def Home(request):
    if request.method == "POST":
        category = request.POST.get('category'),
        bank_name = request.POST.get('bank_name'),
        bsb = request.POST.get('bsb'),
        business_name = request.POST.get('business_name'),
        business_desc = request.POST.get('business_desc'),
        business_address = request.POST.get('business_address'),
        email = request.POST.get('email'),
        In = request.POST.get('In'),
        subcategory = request.POST.get('subcategory'),
        Account_holder = request.POST.get('Account_holder'),
        account_number = request.POST.get('account_number'),
        business_contact = request.POST.get('business_contact'),
        image1 = request.FILES.get('image1'),
        add_offer = request.POST.get('add_offer')
        obj = business_details(category=request.POST['category'],
                               bank_name=request.POST['bank_name'],
                               bsb=request.POST['bsb'],
                               business_name=request.POST['business_name'],
                               business_desc=request.POST['business_desc'],
                               business_address=request.POST['business_address'],
                               email=request.POST['email'],
                               In=request.POST['In'],
                               subcategory=request.POST['subcategory'],
                               Account_holder=request.POST['Account_holder'],
                               account_number=request.POST['account_number'],
                               business_contact=request.POST['business_contact'],
                               image1=request.FILES['image1'],
                               add_offer=request.POST['add_offer'],
                               )
        obj.save()
    # return redirect('/home')
    return render(request, "business.html")


def percentage(part, whole):
    return 100 * float(part)/float(whole)

    print(percentage(5, 7))

    print('{:.2f}'.format(percentage(5, 7)))
    return render(request, "tables.html")


def tablelist(request):
    movies = business_details.objects.all()
    codes = Transactions.objects.all()
    
    context = {"movie": movies, "codes": codes, "host": 'http://13.232.49.240:8000'}


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
        username = request.POST['username'],
        lastname = request.POST['lastname'],
        phone = request.POST['phone'],
        email = request.POST['email'],
        password1 = request.POST['password1'],
        password2 = request.POST['password2'],
        customercode = request.POST['customercode'],
        communitycode = request.POST['communitycode'],
        salescode = request.POST['salescode'],
        obj = User.objects.create(username=username,
                                  lastname=lastname,
                                  phone=phone,
                                  email=email,
                                  password1=password1,
                                  password2=password2,
                                  customercode=customercode,
                                  communitycode=communitycode,
                                  salescode=salescode,)
        obj.save()
        return redirect('/notification.html', {'obj': obj})


# def my_view(request):
#     # Build context for rendering QR codes.
#     context = dict(
#         my_options=QRCodeOptions(size='t', border=6, error_correction='L'),
#     )

#     # Render the view.
#     return render(request, 'page-403.html', context=context)
