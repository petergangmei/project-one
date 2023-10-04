from rest_framework import serializers
from django.contrib.auth.models import User
# from account.models import *
from django.contrib.auth.hashers import make_password
from account.models import PasswordReset
from core.utils import generate_otp, generate_username
from django.utils import timezone
import jwt
from core.utils import send_email
from django.conf import settings
from projectone.models import *

class UserProfileUpdate(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255,style={'input_type':'text',},write_only=True)
    last_name = serializers.CharField(max_length=255,style={'input_type':'text',},write_only=True)
    class meta:
        model = User
        fields = ['email','first_name', 'last_name']

    def validate(self, attrs):
        fname = attrs.get('first_name')
        lname = attrs.get('last_name')
        email = attrs.get('email')
        if email is None:
            raise serializers.ValidationError({'email':'Please provide user email.'})
        return attrs
class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255,style={'input_type':'email',},write_only=True)
    class Meta:
        fields = ['email']
        
class UserChangePasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255,style={'input_type':'hidden',},write_only=True)
    otp = serializers.CharField(max_length=255,style={'input_type':'number',},write_only=True) 
    password = serializers.CharField(max_length=255,style={'input_type':'password',},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password',},write_only=True)
    class Meta:
        fields = ['email','otp','password', 'password2']

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        userObj = User.objects.get(email=email)
        try:
            pas = PasswordReset.objects.get(user=userObj, valid_til__gt=timezone.now(),password_updated=False)
            if pas.password_updated is True:
                raise serializers.ValidationError({'token':'This token has already been used.'})
            
            print('stored otp:', pas.otp)
            print('given otp:', otp)
            if str(pas.otp) != str(otp):
                raise serializers.ValidationError({'token':'Invalid OTP.'})

        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError({'token':'This token is not valid anymore'})
        if password != password2:
            raise serializers.ValidationError({'password':'Password and confirm password does not match!'})
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        pas =PasswordReset.objects.get(user=userObj, valid_til__gt=timezone.now(),password_updated=False)
        pas.password_updated=True
        pas.save()
        return attrs
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']

class TopCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'about', 'slug']

class TopCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['slug']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'about']

    def validate(self, attrs):
        name = attrs.get('name')
        about = attrs.get('about')

        if len(name) <3:
            raise serializers.ValidationError({'name':'Please enter name with more than 3 characters'})
        if len(about) <5:
            raise serializers.ValidationError({'name':'About required at least 5 characters'})
        return attrs
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Make password write-only for security
    class Meta:
        model = User
        fields = ['email','username', 'password']

    def create(self , validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
