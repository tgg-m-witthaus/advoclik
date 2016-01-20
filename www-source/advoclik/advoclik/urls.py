from django.conf.urls import patterns, include, url
from .settings import base
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', include('home.urls')),
    url(r'^admin/', admin.site.urls),
]
