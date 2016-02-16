from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class facebook_data(models.Model):
    user = models.ForeignKey(User)
    friend_count = models.IntegerField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
