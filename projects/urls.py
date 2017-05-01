from django.conf.urls import url
from home.views import (
    project_detail
)
from .views import project_comments, project_updates
urlpatterns = [
    url(r'^(?P<id>\d+)/$', project_detail, name='project_detail'),
    url(r'^(?P<id>\d+)/project_comments/', project_comments, name='project_comments'),
    url(r'^(?P<id>\d+)/project_updates/', project_updates, name='project_updates'),
]