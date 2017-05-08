from django.conf.urls import url
from home.views import (
    project_detail,
    pledge_add,
    project_delete,
    project_edit,
)
from .views import (

    ProjectLikeRedirect,
    ProjectLikeAPIToggle,
    project_explore,
    project_rate,
    project_complete,
    project_update
)
urlpatterns = [
    url(r'^(?P<id>\d+)/$', project_detail, name='project_detail'),
    url(r'^(?P<id>\d+)/edit', project_edit, name='project_edit'),
    url(r'^(?P<id>\d+)/rate/', project_rate, name='project_rate'),
    url(r'^(?P<id>\d+)/delete/', project_delete, name='project_delete'),
    url(r'^(?P<id>\d+)/update/', project_update, name='project_update'),
    url(r'^(?P<id>\d+)/complete/', project_complete, name='project_complete'),
    url(r'^(?P<id>\d+)/pledge_add/', pledge_add, name='pledge_add'),
    url(r'^(?P<id>\d+)/like/', ProjectLikeRedirect.as_view(), name='like_toggle'),
    url(r'^api/(?P<id>\d+)/like/', ProjectLikeAPIToggle.as_view(), name='api_like_toggle'),
    url(r'^explore/', project_explore, name='project_explore'),
]