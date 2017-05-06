from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Projects, CreditCards, Pledges, Charges
from django.conf import settings
import datetime
from projects.forms import ProjectCreateForm
from django.contrib.auth import get_user_model
from .forms import CreditCardAddForm, PledgeAddForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your views here.

User = get_user_model()

def index(request):
    return render(request, 'homebase.html')


def project_create(request):
    form = ProjectCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.uid = User.objects.get(id=request.user.id)
        print("image")
        print(project.image)
        project.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(project.get_project_detail)
    context = {
        "form": form,
        "title": 'Project Create'
    }
    return render(request, "projects/project_create.html", context)


def project_detail(request, id=None):
    instance = get_object_or_404(Projects, id=id)
    context = {
        "project_name": instance.pname,
        "project_id": instance.id,
        "project_minimum_amount": instance.minimum_amount,
        "project_maximum_amount": instance.maximum_amount,
        "days": (instance.end_date - datetime.date.today()).days,
        "project_backers": instance.pledged_people_num,
        "project_amount_pledged": instance.pledged_amount,
        "project_description": instance.description,
        "project_percent": (instance.pledged_amount / instance.minimum_amount) * 100,
        "project_status": instance.status,
        "instance": instance
    }
    return render(request, "projects/project_detail.html", context)

def project_list(request):
    queryset = Projects.objects.filter(uid_id=request.user.id)
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "home/project_list.html", context)

def project_update(request):
    return HttpResponse("<h1>Hello!</h1>")


def project_delete(request):
    return HttpResponse("<h1>Hello!</h1>")

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
