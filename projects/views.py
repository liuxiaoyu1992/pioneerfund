from django.shortcuts import render, get_object_or_404
from home.models import Projects
import datetime
from .forms import ProjectCreateForm


# Create your views here.
def project_comments(request, id=None):
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
    return render(request, 'projects/project_comments.html', context)

def project_updates(request, id=None):
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
    return render(request, 'projects/project_updates.html', context)