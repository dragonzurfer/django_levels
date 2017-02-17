from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    rank=models.IntegerField(default=0)
    points=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('auth:index')

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)