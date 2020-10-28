from django.contrib import admin
from .models import file_info,file_storage

admin.site.register(file_info)
admin.site.register(file_storage)
