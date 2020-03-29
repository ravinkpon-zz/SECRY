from django.contrib import admin
from .models import file_info,file_storage

# Register your models here.
admin.site.register(file_info)
admin.site.register(file_storage)
