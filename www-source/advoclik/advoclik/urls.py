from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('home.urls', namespace='advoclik')),
    url(r'^auth/', include('thirdauth.urls', namespace='thirdauth')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url('social/', include('social.apps.django_app.urls', namespace='social')),
    # url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', admin.site.urls),
]

# I'm disabling all the auth stuff cause it looks for specific login and registration urls

# Eventually should integrate, but leaving this for now as it appear to work
