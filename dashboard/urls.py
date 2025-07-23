from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("swot/",views.dashboard,name="swot"),
   
]
