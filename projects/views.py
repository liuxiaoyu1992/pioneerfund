from django.shortcuts import render, get_object_or_404, redirect
from home.models import Projects
import datetime
from .forms import ProjectCreateForm
from django.views.generic import RedirectView
from .forms import ProjectRateForm, ProjectUpdateForm
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()


class ProjectLikeRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs.get("id")
        print(id)
        obj = get_object_or_404(Projects, id=id)
        url_ = obj.get_project_detail()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class ProjectLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Projects, id=id)
        url_ = obj.get_project_detail()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)

def project_explore(request):
    return render(request, 'explore.html')

def project_rate(request, id=None):
    form = ProjectRateForm(request.POST or None)
    if form.is_valid():
        rate = form.save(commit=False)
        rate.uid = User.objects.get(id=request.user.id)
        rate.pid_id = id
        rate.save()


        url_ = "/projects/" + str(id)
        return redirect(url_)
    context = {
        "form": form,
        "title": 'Rate'
    }
    return render(request, "projects/project_create.html", context)

def project_complete(request, id=None):
    project = Projects.objects.get(id=id)
    print(id)
    print(project.status)
    project.status = 'completed'
    print(project.status)
    project.save()
    return redirect("home:project_list")

def project_update(request, id=None):
    form = ProjectUpdateForm(request.POST or None)
    if form.is_valid():
        rate = form.save(commit=False)
        rate.uid = User.objects.get(id=request.user.id)
        rate.pid_id = id
        rate.save()

        url_ = "/projects/" + str(id)
        return redirect(url_)
    context = {
        "form": form,
        "title": 'Project process update'
    }
    return render(request, "projects/project_create.html", context)