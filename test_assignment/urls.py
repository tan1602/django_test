from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^myapp/', include('myapp.url')),
]