from django.urls import path
from . import views
from django.conf.urls import url
from secry import settings
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',views.home,name='home'),
    path('change',views.change, name='change'),
    url(r'^logout/$', LogoutView.as_view(),{'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('login', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('contactus', views.contact, name='contact'),
    path('response_password', views.change_password, name='changepassword'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.change_pass_link, name='change_pass_link'),
]
