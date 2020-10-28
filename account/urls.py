from django.urls import path
from . import views
from secry import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/profile', views.dash, name='dash'),
    path('accounts/upload', views.upload, name='upload'),
    path('accounts/download', views.download, name='download'),
    path('accounts/dashboard',views.account,name='account'),
    path('accounts/settings', views.settings, name='settings'),
    path('accounts/edituser', views.edituser, name='edituser'),
    path('accounts/changepass', views.changepass, name='changepass'),
    path('accounts/view', views.view, name='view'),
    path('accounts/generate', views.generate, name='generate'),
    path('accounts/download_file', views.download_file, name='download_file'),
    path('accounts/upload_file', views.upload_file, name='upload_file'),
    path('accounts/delete_file', views.delete_file, name='delete_file'),
    path('accounts/delete_account', views.delete_account, name='delete_account'),
]