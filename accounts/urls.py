from django.conf.urls import url, include

from . import views
from home.views import index
from .views import (
    UserDetailView,
    UserFollowView,
    edit_profile
    )
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.log_out_view, name='logout'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^edit_profile/', views.edit_profile, name='edit_profile'),
    url(r'^edit_personal_profile/', views.edit_personal_profile, name='edit_personal_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^tohome/', index, name='tohome'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),
    # url(r'^accounts/', include('registration.backends.simple.urls')),
]