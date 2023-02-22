from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


from authentication.models import User
from rest_framework import serializers

# User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     username = attrs.get('username')
    #     password = attrs.get('password')
        

    #     # if username and password:
    #     #     user = authenticate(
    #     #         request=self.context.get('request'),
    #     #         username=username,
    #     #         password=password
    #     #     )

    #     #     if not user:
    #     #         msg = ('Unable to authenticate with provided credentials',)
    #     #         raise serializers.ValidationError(msg=msg,code='authetication')
    #     #     else:
    #     #      attrs['user'] = user
    #     if email and password:
    #         user = authenticate(
    #             request=self.context.get('request'),
    #             email=email,
    #             password=password
    #         )

    #         if not user:
    #             msg = ('Unable to authenticate with provided credentialsdfs',)
    #             raise serializers.ValidationError(msg=msg,code='authetication')
    #         else:
    #          attrs['user'] = user

    #     else:
    #             msg = ('Must include "username" and "password".')
    #             raise serializers.ValidationError(msg, code='authorization')
        
    #     return
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    # def validate(self, attrs):
    #     email = attrs.get('email', '')
    #     if email:
    #         if User.objects.filter(email=email).exists():
    #             raise serializers.ValidationError(
    #                 {'email': ('Email is already in use')})
    #     return super().validate(attrs)

    def create(self, validated_data):
        password_data = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password_data)
        user.save()
        return user
    

class RegisterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password_data = validated_data.pop('password')
        user = User.objects.create_superuser(**validated_data)
        user.set_password(password_data)
        user.save()
        return user