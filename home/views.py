from django.shortcuts import render
from django.http import HttpResponse
from .models import Projects

# Create your views here.
def index(request):
    return render(request, 'homebase.html')


def project_create(request):
    return HttpResponse("<h1>Hello!</h1>")


def project_detail(request):
    return HttpResponse("<h1>Hello!</h1>")

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
