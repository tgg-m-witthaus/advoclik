from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^initialize', views.index, name='initialize'),
    url(r'refer/(?P<url_suffix>.*)/$', views.referral_redirect, name='referral_link'),
    url(r'campaigns/$', views.campaigns, name='campaigns'),
    url(r'campaigns/results/(?P<campaign_id>[0-9]+)/$', views.campaign_summary, name='campaign_click_summary')
]
