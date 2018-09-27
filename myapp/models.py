from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    middle_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)

