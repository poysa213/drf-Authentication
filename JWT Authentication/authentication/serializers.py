from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers


import requests
from dotenv import load_dotenv
import os

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
        # email = self.context.request.data.get('email', '')
        if len(email) == 0:
            raise ValidationError('enter valid email!')
        response = requests.get('https://api.hunter.io/v2/email-verifier?email='+ email + '&api_key='+ os.environ.get('API_KEY'))
        response = response.json()
        if(response.get("data", {}).get("status", "") == "valid"):
            return email
        raise ValidationError('Enter valid email address!')
        
    
    def create(self, validated_data):
        password_data = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password_data)
        user.save()
        return user
    
