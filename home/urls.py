from django.conf.urls import url, include
from accounts.views import log_out_view
from .views import (
    index,
    project_list,
    project_create,
    payment_methods,
    creditcard_add,
    creditcard_delete
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^logout/', log_out_view, name='logout'),
    url(r'^myprojects/', project_list, name='project_list'),
    url(r'^project_create/', project_create, name='project_create'),
    url(r'^payment_methods/', payment_methods, name='payment_methods'),
    url(r'^creditcard_add/', creditcard_add, name='creditcard_add'),
    url(r'^creditcard_delete/(?P<id>\d+)/', creditcard_delete, name='creditcard_delete'),
]