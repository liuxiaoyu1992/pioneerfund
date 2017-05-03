from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Projects, CreditCards
from django.conf import settings
import datetime
from projects.forms import ProjectCreateForm
from django.contrib.auth import get_user_model
from .forms import CreditCardAddForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.

User = get_user_model()

def index(request):
    return render(request, 'homebase.html')


def project_create(request):
    form = ProjectCreateForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.uid = User.objects.get(id=request.user.id)
        image = form.cleaned_data['image']
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
        "days": (datetime.date.today() - instance.end_date).days,
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

