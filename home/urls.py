from django.urls import path
from . import views
from django.conf.urls import url
from secry import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('change',views.change, name='change_password'),
    url(r'^logout/$', views.signout,{'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
    path('login', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('contactus', views.contact, name='contact'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]
