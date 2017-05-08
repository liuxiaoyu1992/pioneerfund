from django.conf.urls import url, include


from home.views import index as homeindex
from .views import (
    index,
    login_view,
    log_out_view,
    register_view,
    edit_profile,
    edit_personal_profile,
    change_password,
    UserDetailView,
    UserFollowView,
    edit_profile
    )
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', log_out_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    url(r'^edit_profile/', edit_profile, name='edit_profile'),
    url(r'^edit_personal_profile/', edit_personal_profile, name='edit_personal_profile'),
    url(r'^change_password/$', change_password, name='change_password'),
    url(r'^tohome/', homeindex, name='tohome'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),
    # url(r'^accounts/', include('registration.backends.simple.urls')),
]