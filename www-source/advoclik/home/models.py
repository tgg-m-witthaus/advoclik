from __future__ import unicode_literals

from django.db import models
from advoclik.models import MyUser
from datetime import datetime, timedelta
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your models here.

@python_2_unicode_compatible
class Vendor(models.Model):
    name = models.CharField(max_length=30)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=12)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Campaign(models.Model):
    vendor_id = models.ForeignKey('Vendor')
    campaign_name = models.CharField(max_length=30)
    created_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=False)
    target_clicks = models.IntegerField()

    def __str__(self):
        return self.campaign_name

    def get_img_path(self):
        return static('img/'+self.campaign_name+'.jpg')

    def details_url(self):
        return "/home/campaigns/results/" + str(self.id)


@python_2_unicode_compatible
class ReferralLink(models.Model):
    user_id = models.ForeignKey(MyUser)
    campaign_id = models.ForeignKey('Campaign')
    referral_url = models.CharField(max_length=50)
    redirect_url = models.URLField(max_length=200)
    referral_suffix = models.CharField(max_length=50)

    def __str__(self):
        return self.referral_url

@python_2_unicode_compatible
class ReferralClick(models.Model):
    link = models.ForeignKey(ReferralLink)
    campaign = models.ForeignKey(Campaign)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=50, null=True)
    origin = models.CharField(max_length=50, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link + self.pub_date
