from django.conf.urls import url, include
from accounts.views import log_out_view
from .views import (
    index,
    project_list,
    project_create
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^logout/', log_out_view, name='logout'),
    url(r'^myprojects/', project_list, name='project_list'),
    url(r'^project_create/', project_create, name='project_create'),
]