from django.conf.urls import url, include

from . import views
from home.views import index
from .views import (
    UserDetailView,
    UserFollowView
    )
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.log_out_view, name='logout'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^tohome/', index, name='tohome'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),
    # url(r'^accounts/', include('registration.backends.simple.urls')),
]