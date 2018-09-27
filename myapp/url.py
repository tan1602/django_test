from django.conf.urls import url
from django.urls import path, re_path

from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [

    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^register', views.RegistrationView.as_view(), name='register'),
    url(r'^password_reset', views.PasswordResetView.as_view(), name='pass_reset'),
    path(r'^dash/<name>$', views.DashView.as_view(), name='dash'),
    #url(r'^successful_login/logout/$', views.logout, name='u_logout'),
]