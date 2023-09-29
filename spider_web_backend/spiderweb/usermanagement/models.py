from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login,logout,authenticate

class User(AbstractUser):
    USERNAME_FIELD = 'username'