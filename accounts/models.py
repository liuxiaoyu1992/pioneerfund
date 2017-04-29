from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.




class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, blank=False)
    interests = models.CharField(max_length=100, blank=False)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)