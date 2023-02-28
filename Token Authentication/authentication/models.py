from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib import admin
import uuid



class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    objects = UserManager()
    
    
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.email

  
   