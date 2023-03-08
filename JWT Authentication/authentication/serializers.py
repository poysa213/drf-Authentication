from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')



class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        password_data = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password_data)
        user.save()
        return user
    
