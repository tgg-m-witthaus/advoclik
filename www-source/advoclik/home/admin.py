from django.contrib import admin
from.models import User, ReferralLink, ReferralClick, Campaign, Vendor

# Register your models here.

admin.site.register(ReferralLink)
admin.site.register(ReferralClick)
admin.site.register(Campaign)
admin.site.register(Vendor)