from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Projects, CreditCards, Pledges, Charges, Rates, Project_updates
from django.conf import settings
import datetime
from projects.forms import ProjectCreateForm
from django.contrib.auth import get_user_model
from .forms import CreditCardAddForm, PledgeAddForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
import datetime
from django.db.models import Q
from django.views.generic import DetailView

# Create your views here.

User = get_user_model()

def index(request):
    # personal activities
    # user_profiles = UserProfile.objects.filter(following__id=request.user.id).values()
    # following_users = []
    # print(user_profiles)
    # for up in user_profiles:
    #     following_users.append(up['user'])
    # print(following_users)

    # projects = Projects.objects.filter(uid__userprofile__in=UserProfile.objects.get(user=request.user).following.all())
    projects = Projects.objects.filter(uid__id=request.user.id).order_by('-created_at')[:10].values()
    recent_created_projects = projects
    # for proj in projects:
    #     recent_created_projects.append([proj['pname'], proj['created_at']])
    pledges = Pledges.objects.filter(uid__id=request.user.id).order_by('-ptime')[:10].values()
    recent_pledges = pledges
    for plg in pledges:
        plg['pid_id'] = Projects.objects.get(id=plg['pid_id']).pname

    print(recent_pledges)
    context = {
        "recent_created_projects": recent_created_projects,
        "recent_pledges": recent_pledges
    }
    return render(request, 'homebase.html', context)

# class IndexView(DetailView):
#     template_name = 'accounts/user_detail.html'
#     queryset = User.objects.all()
#
#     def get_object(self):
#         return get_object_or_404(
#             User,
#             username__iexact=self.kwargs.get("username")
#         )
#
#
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(IndexView, self).get_context_data(*args, **kwargs)
#         following = UserProfile.objects.is_following(self.request.user, self.get_object())
#         print(following)
#         my_pledges = Pledges.objects.filter(uid__username=self.kwargs.get("username")).values()
#         project_ids = set()
#         for pled in my_pledges:
#             project_ids.add(pled['pid_id'])
#         my_filter_qs = Q()
#         for project_id in project_ids:
#             my_filter_qs = my_filter_qs | Q(id=project_id)
#         backed_projects = Projects.objects.filter(my_filter_qs)
#
#         context['following'] = following
#         context['created_projects'] = Projects.objects.filter(uid__username=self.kwargs.get("username"))
#         context['backed_projects'] = backed_projects
#         context['profiles'] = UserProfile.objects.get(user__username=self.kwargs.get("username"))
#
#
#         print(context)
#         return context


def project_create(request):
    form = ProjectCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.uid = User.objects.get(id=request.user.id)
        print("image")
        print(project.image)
        project.save()
        form.save_m2m()
        messages.success(request, "Successfully Created")
        url_ = "/projects/" + str(project.id)
        return redirect(url_)
    context = {
        "form": form,
        "title": 'Project Create'
    }
    return render(request, "projects/project_create.html", context)


def project_detail(request, id=None):
    instance = get_object_or_404(Projects, id=id)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    percent = 100 * float(instance.pledged_amount) / float(instance.minimum_amount)
    # if percent > 100
    percent = "%.2f" % percent
    form = CommentForm(request.POST or None, initial=initial_data)
    rate_permission = 0
    already_rated = 0
    if Pledges.objects.filter(uid__id=request.user.id).count() > 0:
        rate_permission = 1
    if Rates.objects.filter(pid__id=id, uid__id=request.user.id).count() == 1:
        already_rated = 1
    project_rated = 0
    if Rates.objects.filter(pid__id=id).count() > 0:
        project_rated = 1
    rates = Rates.objects.filter(pid__id=id).values()
    stars = []
    for rate in rates:
        stars.append(rate['star'])
    avg_rate = 0
    if len(stars) > 0:
        avg_rate = sum(stars) / float(len(stars))
    updates = Project_updates.objects.filter(pid__id=id, uid__id=request.user.id)


    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_project_detail())

    comments = instance.comments
    context = {
        "project_name": instance.pname,
        "project_id": instance.id,
        "project_minimum_amount": instance.minimum_amount,
        "project_maximum_amount": instance.maximum_amount,
        "days": (instance.end_date - datetime.date.today()).days,
        "project_backers": instance.pledged_people_num,
        "project_amount_pledged": instance.pledged_amount,
        "project_description": instance.description,
        "project_percent": percent,
        "project_status": instance.status,
        "instance": instance,
        "comments": comments,
        "comment_form": form,
        "rate_permission": rate_permission,
        "already_rated": already_rated,
        "project_rated": project_rated,
        "avg_rate": avg_rate,
        "project_updates": updates
    }
    return render(request, "projects/project_detail.html", context)

def project_list(request):
    queryset = Projects.objects.filter(uid_id=request.user.id)
    context = {
        "object_list": queryset,
        "user_id": request.user.id,
        "title": "My projects"
    }
    print(context)
    return render(request, "home/project_list.html", context)

def project_back_list(request):
    my_pledges = Pledges.objects.filter(uid__id=request.user.id).values()
    print(request.user.id)
    print(my_pledges)
    project_ids = set()
    if my_pledges:
        for pled in my_pledges:
            project_ids.add(pled['pid_id'])
            print("uid")
            print(pled['uid_id'])
        my_filter_qs = Q()
        for project_id in project_ids:
            my_filter_qs = my_filter_qs | Q(id=project_id)
        queryset = Projects.objects.filter(my_filter_qs)
    else:
        queryset = None
    context = {
        "object_list": queryset,
        "title": "Projects backed"
    }
    return render(request, "home/project_list.html", context)

def project_pledges(request):
    queryset = Pledges.objects.filter(uid_id=request.user.id)
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "home/project_pledges.html", context)

def project_charges(request):
    queryset = Charges.objects.filter(uid_id=request.user.id)
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "home/project_charges.html", context)

def project_likes(request):
    queryset = Projects.objects.filter(likes__id=request.user.id)
    print(queryset)
    context = {
        "object_list": queryset,
        "title": "Project liked"
    }
    return render(request, "home/project_list.html", context)

def project_edit(request, id=None):
    instance = get_object_or_404(Projects, id=id)
    form = ProjectCreateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        project = form.save(commit=False)
        project.uid = User.objects.get(id=request.user.id)
        project.save()
        form.save_m2m()
        messages.success(request, "Successfully Edited")
        url_ = "/projects/" + str(project.id)
        return redirect(url_)
    context = {
        "form": form,
        "title": 'Project edit'
    }
    return render(request, "projects/project_create.html", context)


def project_delete(request, id=None):

    instance = get_object_or_404(Projects, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("home:project_list")

def payment_methods(request):
    queryset = CreditCards.objects.filter(uid_id=request.user.id)
    context = {
        "object_list": queryset,
        "title": "Credit cards"
    }
    return render(request, 'home/payment_methods.html', context)

def creditcard_add(request):
    form = CreditCardAddForm(request.POST or None)
    if form.is_valid():
        creditcatd = form.save(commit=False)
        creditcatd.uid = User.objects.get(id=request.user.id)
        creditcatd.save()
        return redirect("/home/payment_methods")
    context = {
        "form": form,
        "title": "Add Credit Card"
    }
    return render(request, "home/creditcard_add.html", context)

def creditcard_delete(request, id=None):
    instance = get_object_or_404(CreditCards, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("home:payment_methods")

def pledge_add(request, id=None):
    form = PledgeAddForm(request.POST or None, user=request.user)
    instance = get_object_or_404(Projects, id=id)
    if form.is_valid():
        pledge = form.save(commit=False)
        pledge.uid = User.objects.get(id=request.user.id)
        pledge.pid_id = id
        pledge.save()
        return HttpResponseRedirect(instance.get_project_detail())
    context = {
        "form": form,
        "title": "Pledge",
        "instance": instance
    }
    return render(request, "home/pledge_add.html", context)

@receiver(post_save, sender=Pledges)
def pledge_to_project(sender, instance, created, **kwargs):
    if created:
        print("pid")
        print(instance.pid.id)
        print(instance.amount)
        project = Projects.objects.get(id=instance.pid.id)
        project.pledged_amount += instance.amount
        print("uid")
        print(instance.uid_id)
        count = Pledges.objects.filter(uid_id=instance.uid_id, pid_id=instance.pid.id).count()
        print("count")
        print(count)
        if count == 1:
            project.pledged_people_num += 1
        if project.pledged_amount >= project.maximum_amount:
            project.status = 'pledge succeeded'
            pledge = Pledges.objects.filter(pid=instance.pid)
            for pled in pledge:
                Charges.objects.create(
                    uid_id=pled.uid_id,
                    pid_id=pled.pid_id,
                    amount=pled.amount,
                    ptime=pled.ptime,
                    charge_time=datetime.datetime.now(),
                    cnum_id=pled.cnum_id,

                )
                pledtemp = pled
                pledtemp.status = 'succeeded'
                pledtemp.save()
        project.save()
