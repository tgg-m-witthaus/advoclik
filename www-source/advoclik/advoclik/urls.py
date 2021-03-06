from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import logout
urlpatterns = [
    url(r'^home/', include('home.urls', namespace='advoclik')),
    url(r'^$', RedirectView.as_view(url='/landing/')),
    url(r'^auth/', include('thirdauth.urls', namespace='thirdauth')),
    url(r'^landing/', include('landing.urls', namespace='landing')),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url('social/', include('social.apps.django_app.urls', namespace='social')),
    # url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', admin.site.urls),
]

# I'm disabling all the auth stuff cause it looks for specific login and registration urls

# Eventually should integrate, but leaving this for now as it appear to work
