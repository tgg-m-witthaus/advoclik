from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from django.contrib.auth.models import Group
from django.core.mail import send_mail
import os
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.db.models import Q
from django.db.models import Count
from advoclik.models import MyUser

from .models import ReferralLink, ReferralClick, Campaign


# Create your views here.
@login_required
def index(request):
    # Note: Images are handled really shittily
    campaigns = Campaign.objects.all()
    links = ReferralLink.objects.all()
    context = {'links': links, 'campaigns': campaigns}
    return render(request, 'home/home.html', context)

@login_required
def campaigns(request):
    # I wonder if this is doing two separate queries or if it is smart enough to not duplicate work. No idea
    campaign_list = Campaign.objects.annotate(num_clicks=Count('referralclick__ip_address'), num_unique_ip=Count('referralclick__ip_address', distinct=True))
    # campaign_list = Campaign.objects.all()
    context = {'campaigns': campaign_list}
    return render(request, 'home/campaigns.html', context)

@login_required
def campaign_summary(request, campaign_id):

    campaign = Campaign.objects.get(pk=campaign_id)
    clicks = ReferralClick.objects.filter(campaign=campaign)
    context = {'clicks': clicks, 'campaign': campaign}
    return render(request, 'home/campaign_click_summary.html', context)


def referral_redirect(request, url_suffix):
    refer = get_object_or_404(ReferralLink, referral_suffix__exact=url_suffix)
    redirect_url = refer.redirect_url

    click = ReferralClick(link=refer,
                          campaign=refer.campaign_id,
                          ip_address=get_client_ip(request),
                          user_agent=request.META.get('HTTP_USER_AGENT'),
                          origin=request.META.get('HTTP_REFERER'))

    click.save()

    #redirect_url = reverse('index')

    return HttpResponseRedirect(redirect_url)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
