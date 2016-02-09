from django.contrib import admin
from.models import ReferralLink, ReferralClick, Campaign, Vendor
from advoclik.models import MyUser
# Register your models here.

admin.site.register(ReferralLink)
admin.site.register(ReferralClick)
admin.site.register(Campaign)
admin.site.register(Vendor)
