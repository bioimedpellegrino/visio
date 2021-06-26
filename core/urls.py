from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    #Dashboard
    path('main', views.DashboardView.as_view(), name="dashboard"),
]
