from rest_framework import serializers
from authentication.models import Employee, Transactions, deals, payments,business_details,category, rewards
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class business_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = business_details 
        fields="__all__"
        

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields='__all__'
class transSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields='__all__'
class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = payments
        fields="__all__"

class businessSerializer(serializers.ModelSerializer):
    class Meta:
        model = business_details
        fields=('categories',
    'bank_name',
    
    'business_name',
    'business_desc',
    'business_address',
    'email',
    'subcategory',
    'irich',
    
    
    'Account_details',
    'account_number',
    'IFSC_code',
    'business_contact',
    'image1',)
class dealSerializer(serializers.ModelSerializer):
    class Meta:
        model = deals
        fields="__all__"
class rewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = rewards
        fields="__all__"
