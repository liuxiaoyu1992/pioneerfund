from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
# Create your models here.



# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     address = models.CharField(max_length=100, blank=False)
#     city = models.CharField(max_length=30, blank=False)
#     state = models.CharField(max_length=30, blank=False)
#     country = models.CharField(max_length=30, blank=False)
#     interests = models.CharField(max_length=100, blank=False)
#
# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = UserProfile.objects.create(user=kwargs['instance'])
#
# post_save.connect(create_profile, sender=User)

# class CustomUser(AbstractUser):
#     address = models.TextField(max_length=100, blank=False)
#     city = models.TextField(max_length=30, blank=False)
#     state = models.TextField(max_length=30, blank=False)
#     country = models.TextField(max_length=30, blank=False)
#     interests = models.TextField(max_length=100, blank=False)