# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from requests.sessions import session
from authentication.models import Transactions
import os
import stripe



def create_checkout_session(request):
    #  can fetch item and its price here . for now its jsut dumy data
    item_id = request.GET['item_id']
    stripe.api_key = settings.PAYMENT_API_SECRET

    unit_price = 200
    quantity = 1
    session = stripe.checkout.Session.create(
        customer_email='customer@example.com',
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                'name': 'T-shirt',
                },
                'unit_amount': unit_price,
            },
            'quantity': quantity,
        }],
        mode='payment',
        success_url='http://13.232.49.240:8000/payment-success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://13.232.49.240:8000/payment-cancel',
    )

    Transactions(
        price = (unit_price * quantity),
        session_id = session.id,
        status='pending',
        
    ).save()

    return redirect(session.url, code=303)


def payment_success(request):
    stripe.api_key = settings.PAYMENT_API_SECRET
    session_id = stripe.checkout.Session.retrieve(request.GET['session_id'])
    

    transaction = Transactions.objects.filter(
        session_id=request.GET['session_id']
    ).first()

    if transaction is not None:
        # transaction.status = 'success'
        transaction.save()
    else:
        return render(request,'payment_cancel.html')
    
    return render(request,'payment_success.html')

def payment_cancel(request):

    return render(request, 'payment_cancel.html')


@csrf_exempt
def payment_webhook(request):
    payload = request.body

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    endpoint_secret = 'whsec_wjK9VWSMOSneVc997onobJhdoyHx0WP2'
    stripe.api_key = settings.PAYMENT_API_SECRET

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Save an order in your database, marked as 'awaiting payment'
        create_order(session)

        # Check if the order is already paid (e.g., from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            fulfill_order(session)

    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']

        # Fulfill the purchase
        fulfill_order(session)

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']

        # Send an email to the customer asking them to retry their order
        email_customer_about_failed_payment(session)

    # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order(session):
  # TODO: fill me in
  print("Fulfilling order")

def create_order(session):
  # TODO: fill me in
  print("Creating order")

def email_customer_about_failed_payment(session):
  # TODO: fill me in
  print("Emailing customer")

