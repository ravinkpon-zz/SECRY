from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('change',views.change, name='change_password'),
    path('', views.signout, name='signout'),
    path('login', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('contactus', views.contact, name='contact')
    
]
