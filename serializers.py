from rest_framework import serializers
from authentication.models import business_details,category,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class business_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = business_details 
        fields=( 'category',
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
            'add_offer')
class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields=('add_category',)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields=('user',
    'bio',
    'code',
    'recommended_by', 
    'updated', 
    'created',)
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields=('username','email', 'password1', 'password2','communitycode','customercode','phone','lastname','salescode')
#         read_only_fields = ('email','password1', 'password2',)

