
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from advoclik.models import MyUser


@python_2_unicode_compatible
class brandContact(models.Model):
    contact_name = models.CharField(max_length=30)
    contact_email = models.EmailField()
    company = models.CharField(max_length=12)
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s - %s - %s" % (self.company, self.contact_name, self.contact_email)
