from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers


import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()   

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')



class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
   
    def validate_email(self, email):
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email):
            raise ValidationError("Enter a valid Email!")
        if User.objects.filter(email__iexact=email.lower()).exists():
            raise serializers.ValidationError("Email deja exist!")
        response = requests.get('https://api.hunter.io/v2/email-verifier?email='+ email + '&api_key='+ os.environ.get('API_KEY'))
        response = response.json()
        # if(response.get("data", {}).get("status", "") == "valid"):
        #     return email
        # raise ValidationError('THis is NoT a valid email!!!')
        return email
        
    
    def create(self, validated_data):
        password_data = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password_data)
        user.save()
        return user
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['new_password', 'old_password']
    

    def validate_old_password(self, old_password):
        user = self.context.kwargs.get('user', None)
        if user is not None:
            if not user.check_password(old_password):
                raise ValidationError({"old_password": "Old password is not correct"})
            return old_password

    def update(self, instance, validated_data):

        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
