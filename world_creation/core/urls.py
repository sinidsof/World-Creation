
from django.urls import path

from world_creation.core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


# Основни страници
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('feedback/', views.feedback, name='feedback'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

]