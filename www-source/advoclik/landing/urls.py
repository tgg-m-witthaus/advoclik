from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^login', auth_views.login, {'template_name':'landing/login.html'}),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^about', views.about, name='about'),
    url(r'^company', views.company, name='company'),
    url(r'^brands', views.brands, name='brands'),
    url(r'^register_user', views.register_user, name='register_user'),
    url(r'^register', views.register, name='register'),
    url(r'^add_brand_contact', views.add_brand_contact, name='add_brand_contact'),
    url('^', include('django.contrib.auth.urls')),
]
