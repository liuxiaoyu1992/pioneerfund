from django.shortcuts import render, get_object_or_404, redirect
from home.models import Projects, Categories
import datetime
from .forms import ProjectCreateForm
from django.views.generic import RedirectView
from .forms import ProjectRateForm, ProjectUpdateForm
from django.contrib.auth import get_user_model
from django.views import View
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
    instance = Projects.objects.all()

    projects = []
    categories = Categories.objects.all()
    for ins in instance:
        percent = ("%.2f" % (100 * float(ins.pledged_amount) / float(ins.minimum_amount)))
        days = (ins.end_date - datetime.date.today()).days
        pid = ins.id
        uid = ins.uid_id
        pname = ins.pname
        username = ins.uid.username
        first_name = ins.uid.first_name
        last_name = ins.uid.last_name
        backers = ins.pledged_people_num
        pledged_amount = ins.pledged_amount
        description = ins.description
        image = ins.image.url
        projects.append({
            'percent': percent,
            'days': days,
            'uid': uid,
            'username': username,
            'pid': pid,
            'pname': pname,
            'first_name': first_name,
            'last_name': last_name,
            'backers': backers,
            'pledged_amount': pledged_amount,
            'description': description,
            'image': image,
            'instance': ins,
        })
    # percent = (100 * float(instance.pledged_amount) / float(instance.minimum_amount))
    # percent = ("%.2f" % (100 * float(instance.pledged_amount) / float(instance.minimum_amount)))
    context = {
        "projects": projects,
        "categories": categories
        # "days": (instance.end_date - datetime.date.today()).days,
    }
    print(instance)
    return render(request, 'explore.html', context)

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

class SearchView(View):
    def post(self, request, *args, **kwargs):
        if "standard_search" in request.POST:
            words = request.POST["standard_search"]
            instance = Projects.objects.filter(pname__contains=words)
        elif "limit_search" in request.POST:
            category = request.POST["categories"]
            status = request.POST["status"]
            if category == 'allCategories' and status == 'allStatus':
                instance = Projects.objects.all()
            elif category != 'allCategories' and status == 'allStatus':
                instance = Projects.objects.filter(cate_name__id=category)
            elif category == 'allCategories' and status != 'allStatus':
                instance = Projects.objects.filter(status=status)
            else:
                instance = Projects.objects.filter(cate_name__id=category, status=status)
        else:
            instance = None
        projects = []
        for ins in instance:
            percent = ("%.2f" % (100 * float(ins.pledged_amount) / float(ins.minimum_amount)))
            days = (ins.end_date - datetime.date.today()).days
            pid = ins.id
            uid = ins.uid_id
            pname = ins.pname
            username = ins.uid.username
            first_name = ins.uid.first_name
            last_name = ins.uid.last_name
            backers = ins.pledged_people_num
            pledged_amount = ins.pledged_amount
            description = ins.description
            image = ins.image.url
            projects.append({
                'percent': percent,
                'days': days,
                'uid': uid,
                'username': username,
                'pid': pid,
                'pname': pname,
                'first_name': first_name,
                'last_name': last_name,
                'backers': backers,
                'pledged_amount': pledged_amount,
                'description': description,
                'image': image,
                'instance': ins,
            })
        context = {
            "projects": projects,
        }
        return render(request, 'projects/project_search_results.html', context)
