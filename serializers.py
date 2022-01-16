from django.contrib.auth import models
from django.db.models import fields
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

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('id','username','email',)
class UseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('password',)
class EmployeeSerializer(serializers.ModelSerializer):
   

   class Meta:
        model = Employee
        fields=('phone','referral_code','postcode')
class EmployeesSerializer(serializers.ModelSerializer):
   

   class Meta:
        model = Employee
        fields=('phone')
class UserSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = User
        fields = (
            
          'username',
          'password',
          'first_name',
          'last_name',
          'employee','email'
        )

    def create(self, validated_data):
        employee = validated_data.pop('employee')  
        employee = Employee.objects.create(**employee)
        # print(employee.id)
        user = User.objects.create(employee=employee, **validated_data)
        # employee.user_id=user.id
        # employee.save()
        employees=Employee.objects.get(id=employee.id)
        print(employees)
        employees.user_id=user.id
        employees.save()
        return user
class usersSerializer(serializers.ModelSerializer):
    user = UseSerializer()
    class Meta:
        model = Employee
        fields = (
          
          'phone',
          'user'
          
        )

    def create(self, validated_data):
        employee = validated_data.pop('employee')  
        employee = Employee.objects.create(**employee)
        user = User.objects.create(employee=employee, **validated_data)
        
        return user       
    
    
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
