from django.db import models
from django.contrib.auth.models import User
from secry import settings

# Create your models here.

class file_info(models.Model):  # File information model on database
    
    file_id = models.CharField(max_length=10,primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, verbose_name="Category", on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50)
    file_size = models.FloatField(max_length=10)
    file_key = models.CharField(max_length=150)

class file_storage(models.Model):               #file storage model on database
    store_id = models.CharField(max_length=150, primary_key=True)
    content = models.BinaryField()
