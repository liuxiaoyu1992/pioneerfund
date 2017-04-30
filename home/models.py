from django.db import models
import os
from django.conf import settings
# Create your models here.

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    ProjectsModel = instance.__class__
    new_id = ProjectsModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)

class Categories(models.Model):
    # cate_choices = (
    #     ('Medical, Illness & Healing', 'Medical, Illness & Healing'),
    #     ('Funerals & Memorials', 'Funerals & Memorials'),
    #     ('Accidents & Emergencies', 'Accidents & Emergencies'),
    #     ('Education & Learning', 'Education & Learning'),
    #     ('Animals & Pets', 'Animals & Pets'),
    #     ('Sports, Teams & Clubs', 'Sports, Team & Clubs'),
    #     ('Creative Arts, Music & Film', 'Creative Arts, Music & Film'),
    #     ('Missions, Faith & Church', 'Missions, Faith & Church'),
    #     ('Volunteer & Service', 'Volunteer & Service'),
    #     ('Dreams, Hopes & Wishes', 'Dreams, Hopes & Wishes'),
    #     ('Non-Profits & Charities', 'Non-Profits & Charities'),
    #     ('Community & Neighbours', 'Community & Neighbours'),
    #     ('Celebrations & Events', 'Celebrations & Events'),
    #     ('Travel & Adventure', 'Travel & Adventure'),
    #     ('Babies, Kids & Family', 'Babies, Kids & Family'),
    #     ('Weddings & Honeymoons', 'Weddings & Honeymoons'),
    #     ('Business & Entrepreneurs', 'Business & Entrepreneurs'),
    #     ('Competitions & Pageants', 'Competitions & Pageants'),
    #     ('Other', 'Other')
    # )
    catename = models.CharField(max_length=50)

    def __str__(self):
        return self.catename

class Projects(models.Model):
    pname = models.CharField(max_length=50)
    cate_name = models.ForeignKey(Categories, on_delete=models.CASCADE)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    image = models.ImageField(upload_to='project_picture/%y%m%d',
                              null=True,
                              blank=True,
                              )
    description = models.TextField(max_length=5000)
    state = models.CharField(max_length=40, null=True)
    country = models.CharField(max_length=40, null=True)
    minimum_amount = models.FloatField()
    maximum_amount = models.FloatField()
    end_date = models.DateField()
    complete_date = models.DateField(null=True, blank=True)
    pledged_amount = models.FloatField(default=0)
    pledged_people_num = models.IntegerField(default=0)
    status_choices = (
        ('looking for funds', 'looking for funds'),
        ('pledge succeeded', 'pledge succeeded'),
        ('pledge failed', 'pledge failed'),
        ('completed', 'completed')
    )
    status = models.CharField(
        max_length=40,
        choices=status_choices,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class CreditCards(models.Model):
#     cnum = models.CharField(max_length=40, primary_key=True)
#     exp_date = models.DateField()
#     first_name = models.CharField(max_length=40)
#     last_name = models.CharField(max_length=40)
#     uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
#
#
# class Pledges(models.Model):
#     amount = models.FloatField()
#     cnum = models.CharField(max_length=40)
#     uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
#     pid = models.ForeignKey(Projects, on_delete=models.CASCADE)
#     ptime = models.DateTimeField(auto_now_add=True)
#     status = (
#         ('pending', 'pending'),
#         ('succeeded', 'succeeded'),
#         ('failed', 'failed')
#     )
#
#
#
# class Charges:
#     uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
#     pid = models.ForeignKey(Projects, on_delete=models.CASCADE)
#     cnum = models.ForeignKey(CreditCards, on_delete=models.CASCADE)
#     amount = models.FloatField()
#     ptime = models.DateTimeField()
#     charge_time = models.DateTimeField()
#     status = (
#         ('succeeded', 'succeeded'),
#         ('failed', 'failed')
#     )


