from django.contrib import admin
from django.urls import path,include
from .import views

app_name = "dashboard" 

urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard"),
    path("swot/",views.swot,name="swot"),
    path('feasibility/', views.feasibility, name='feasibility'),
    path('risk/', views.risk, name='risk'),
    path("history/", views.history, name="history"),
    path('delete/<int:id>/', views.delete_submission, name='delete'),
<<<<<<< HEAD
    path("ai_sugg/", views.ai_sugg, name="ai_sugg"),
    path("guide/", views.guide, name="guide"),
    path("risk/", views.risk, name="risk"),
=======
    path('update/<int:id>/', views.update_message, name='update'),
>>>>>>> 4d7ed0d66eb218c86dbaa01e3c74a7d3b1a056ce
]
