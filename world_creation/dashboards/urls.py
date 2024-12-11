from django.urls import path
from . import views



urlpatterns = [

    path('creator_dashboard/', views.creator_dashboard, name='creator_dashboard'),
    path('super-creator_dashboard/', views.super_creator_dashboard, name='super_creator_dashboard'),

]