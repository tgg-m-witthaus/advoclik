from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your models here.

@python_2_unicode_compatible
class Vendor(models.Model):
    name = models.CharField(max_length=30)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=12)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Campaign(models.Model):
    vendor_id = models.ForeignKey('Vendor')
    campaign_name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
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
    user_id = models.ForeignKey(User)
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



def init_data():
    user = User.objects.create_user(username="p_kravik", email="pkravik@gmail.com", password="freak123")

    print "maybe"

    tgg_vendor = Vendor(name="TGG", contact_email="tgg@tgggroup.com", contact_phone="3126216060")
    tgg_vendor.save()

    campaign = Campaign(vendor_id=tgg_vendor,
                        campaign_name="Testing",
                        start_date=datetime.strptime("2016-02-01 01:00:00", "%Y-%m-%d %H:%M:%S"),
                        end_date=datetime.strptime("2016-02-08 01:00:00", "%Y-%m-%d %H:%M:%S"),
                        active=True,
                        target_clicks=1000)

    campaign.save()

    link = ReferralLink(user_id=user,
                        campaign_id=campaign,
                        referral_url="refer/test",
                        referral_suffix="test",
                        redirect_url="http://www.tgggroup.com/")

    link.save()





