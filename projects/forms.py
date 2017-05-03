from django import forms
from home.models import Projects


class ProjectCreateForm(forms.ModelForm):
    # pname = forms.CharField(label='Project Name')
    # cate_name = forms.CharField(label='Category')
    # image = forms.CharField(label='Image')
    # state = forms.CharField(label='Project Locate State')
    # country = forms.CharField(label='Project Locate Country')
    # minimum_amount = forms.FloatField(label='Minimum Pledge Amount')
    # maximum_amount = forms.FloatField(label='Maximum Pledge Amount')
    # end_date = forms.DateField(label='Pledge End Date')
    # image = forms.ImageField()
    class Meta:
        model = Projects
        exclude = ["uid"]
        fields = [
            "pname",
            "cate_name",
            "image",
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
            "image": "Image",
            "state": "Project Locate State",
            "country": "Project Locate Country",
            "minimum_amount": "Minimum Pledge Amount",
            "maximum_amount": "Maximum Pledge Amount",
            "end_date": "Pledge End Date"
        }




