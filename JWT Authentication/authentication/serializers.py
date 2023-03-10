from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import validate_password

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



class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[validate_password])

    # class Meta:
    #     model = User
    #     fields = ('email', 'password')
    #     extra_kwargs = {'password': {'write_only' : True}}
   
    def validate_email(self, email :str) -> str :
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email):
            raise ValidationError("Enter a valid Email!")
        if User.objects.filter(email__iexact=email.lower()).exists():
            raise serializers.ValidationError("Email deja exist!")
        # response = requests.get('https://api.hunter.io/v2/email-verifier?email='+ email + '&api_key='+ os.environ.get('API_KEY'))
        # response = response.json()
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
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[validate_password], required=True, write_only=True)
    new_password = serializers.CharField(validators=[validate_password], required=True, write_only=True)
    
   
    

    def validate_old_password(self, old_password : str) -> str:
        validate_password(old_password)
        user = self.context.get('user', None)
        if user is not None:
            if not user.check_password(old_password):
                raise ValidationError({"old_password": "Old password is not correct"})
            return old_password
        
    def validate_new_password(self, new_password):
        validate_password(new_password)
        return new_password
    
    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        if(old_password==new_password):
            raise ValidationError({"error":"you must provide different password!"})
        # Validate old password
        self.validate_old_password(old_password)

        # Validate new password
        self.validate_new_password(new_password)
        return attrs
    
  

   
    def save(self, instance=None, **kwargs):
        user = self.context['user']
        validated_data = kwargs.get('validated_data')

        # I do check for the secon time for security reason !
        if not user.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})
        user.set_password(validated_data['new_password'])
        user.save()
        return user



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
