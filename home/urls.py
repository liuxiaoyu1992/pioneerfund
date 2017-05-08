from django.conf.urls import url, include
from accounts.views import log_out_view
from .views import (
    index,
    project_list,
    project_create,
    payment_methods,
    creditcard_add,
    creditcard_delete,
    project_back_list,
    project_pledges,
    project_charges,
    project_likes
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^logout/', log_out_view, name='logout'),
    url(r'^myprojects/', project_list, name='project_list'),
    url(r'^my_backed_projects/', project_back_list, name='project_back_list'),
    url(r'^my_pledges/', project_pledges, name='project_pledges'),
    url(r'^my_charges/', project_charges, name='project_charges'),
    url(r'^my_likes/', project_likes, name='project_likes'),
    url(r'^project_create/', project_create, name='project_create'),
    url(r'^payment_methods/', payment_methods, name='payment_methods'),
    url(r'^creditcard_add/', creditcard_add, name='creditcard_add'),
    url(r'^creditcard_delete/(?P<id>\d+)/', creditcard_delete, name='creditcard_delete'),
]