from django.conf.urls import url, include
from accounts.views import log_out_view
from .views import (
    project_list
)
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/', log_out_view, name='logout'),
    url(r'^myprojects/', project_list, name='project_list'),

]