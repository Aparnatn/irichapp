import os
from twilio.rest import Client


def send_otp(mobile, otp):
    account_sid = "AC2bade842dde95a6321784a4cd649af9a"
    auth_token = "e1bf226933f4f06cc46c59720008678f"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                              from_='+17542533576',     
                              to=mobile,
                              body=otp
                          ) 

    return "You have successfully delivered the msg"