from rest_framework import serializers
from authentication.models import Transactions, payments,business_details,category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class business_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = business_details 
        fields="__all__"
        

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields=('name','id')
class transSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username','email')
        read_only_fields = ('email','password1', 'password2')
class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = payments
        fields="__all__"

