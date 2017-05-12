from django.db import models
import os
from django.conf import settings
from django.core.urlresolvers import reverse
from .fields import CreditCardField, ExpiryDateField, VerificationValueField
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager

# Create your models here.

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    ProjectModel = instance.__class__
    new_id = ProjectModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "project_picture/%s/%s" %(new_id, filename)

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
    tags = TaggableManager()
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    image = models.ImageField(upload_to=upload_location,
                              default='project_picture/default.png',
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    files = models.FileField(upload_to='files/%y%m%d/', null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='project_likes')
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
        default='looking for funds'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_project_detail(self):
        return reverse("projects:project_detail", kwargs={"id": self.id})

    def get_project_update(self):
        return reverse("projects:project_update", kwargs={"id": self.id})

    def get_project_edit(self):
        return reverse("projects:project_edit", kwargs={"id": self.id})

    def get_project_rate(self):
        return reverse("projects:project_rate", kwargs={"id": self.id})

    def get_project_delete(self):
        return reverse("projects:project_delete", kwargs={"id": self.id})

    def get_project_complete(self):
        return reverse("projects:project_complete", kwargs={"id": self.id})

    def get_project_comments(self):
        return reverse("projects:project_comments", kwargs={"id": self.id})

    def get_pledge_url(self):
        return reverse("projects:pledge_add", kwargs={"id": self.id})

    def get_like_url(self):
        return reverse("projects:like_toggle", kwargs={"id": self.id})

    def get_api_like_url(self):
        return reverse("projects:api_like_toggle", kwargs={"id": self.id})

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

class Project_updates(models.Model):
    pid = models.ForeignKey(Projects, on_delete=models.CASCADE)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    updates = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

RATE_CHOICES = (
    (1, "*"),
    (2, "**"),
    (3, u"***"),
    (4, u"****"),
    (5, u"*****")
)

class Rates(models.Model):
    pid = models.ForeignKey(Projects, on_delete=models.CASCADE)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    star = models.IntegerField(choices=RATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class CreditCards(models.Model):
    cnum = models.CharField(max_length=40)
    exp_date = models.DateField()
    name = models.CharField(max_length=50)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    def __str__(self):
        return self.cnum
#
#
class Pledges(models.Model):
    amount = models.FloatField()
    cnum = models.ForeignKey(CreditCards, on_delete=models.CASCADE)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    pid = models.ForeignKey(Projects, on_delete=models.CASCADE)
    ptime = models.DateTimeField(auto_now_add=True)
    status_choices = (
        ('pending', 'pending'),
        ('succeeded', 'succeeded'),
        ('failed', 'failed')
    )
    status = models.CharField(
        max_length=40,
        choices=status_choices,
        default='pending'
    )



#
#
#
class Charges(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    pid = models.ForeignKey(Projects, on_delete=models.CASCADE)
    cnum = models.ForeignKey(CreditCards, on_delete=models.CASCADE)
    amount = models.FloatField()
    ptime = models.DateTimeField()
    charge_time = models.DateTimeField()
    status_choices = (
        ('succeeded', 'succeeded'),
        ('failed', 'failed')
    )
    status = models.CharField(
        max_length=40,
        choices=status_choices,
        default='succeeded'
    )

class project_view_records(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    pid = models.ForeignKey(Projects, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class tag_search_records(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    tag_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class search_records(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    keyword = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


