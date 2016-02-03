from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^login', auth_views.login, {'template_name':'landing/login.html'}),
    url(r'^logout', auth_views.logout, name='logout'),
    url('^', include('django.contrib.auth.urls')),
]
