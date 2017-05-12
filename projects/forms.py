from django import forms
from home.models import Projects, Rates, Project_updates


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ["uid"]
        fields = [
            "pname",
            "cate_name",
            "tags",
            "image",
            "files",
            "state",
            "country",
            "description",
            "minimum_amount",
            "maximum_amount",
            "end_date",
        ]

        labels = {
            "pname": "Project Name",
            "cate_name": "Category",
            "tags": "Tags",
            "image": "Image",
            "files": "Files",
            "state": "Project Locate State",
            "country": "Project Locate Country",
            "minimum_amount": "Minimum Pledge Amount",
            "maximum_amount": "Maximum Pledge Amount",
            "end_date": "Pledge End Date"
        }

class ProjectRateForm(forms.ModelForm):
    class Meta:
        model = Rates
        exclude = ["uid", "pid"]
        fields = [
            "star"
        ]
        labels = {
            "star": "Star"
        }

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project_updates
        exclude = ["uid", "pid"]
        fields = [
            "updates"
        ]
        labels = {
            "updates": "Updates"
        }
