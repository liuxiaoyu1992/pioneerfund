from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/', views.login_view, name='login'),
    # url(r'^logout/', views.log_out_view, name='logout'),
    # url(r'^register/', views.register_view, name='register'),
    # url(r'^accounts/', include('registration.backends.simple.urls')),
]