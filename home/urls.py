from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.home,name='home'),
    path('change',views.change, name='change_password'),
    path('', views.signout, name='signout'),
    path('login', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('contactus', views.contact, name='contact'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]
