from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.CharField(max_length=10,primary_key=True)
    phone = models.BigIntegerField(blank=True)
    location = models.CharField(max_length=30, blank=True)