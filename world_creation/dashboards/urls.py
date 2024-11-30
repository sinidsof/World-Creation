from django.urls import path
from . import views

# urlpatterns = [
#     # Други пътища
#     path('tasks/<int:task_id>/assessment-dashboards/', views.assessment_feedback, name='assessment_feedback'),
# ]

urlpatterns = [
    path('creator_dashboard/', views.creator_dashboard, name='creator_dashboard'),
    # path('tasks/<int:task_id>/assessment-dashboards/<int:self_assessment_id>/', views.assessment_feedback, name='assessment_feedback'),
    path('super-creator_dashboard/', views.super_creator_dashboard, name='super_creator_dashboard'),
]