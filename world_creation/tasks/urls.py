
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.TaskListView.as_view(), name='task_list'),  # Страница със списък със задачи
    path('create/', views.create_task, name='create_task'),  # Страница за създаване на задачи
    path('<int:task_id>/', include([

        path('edit/', views.EditTaskView.as_view(), name='edit_task'),  # Редактиране на задача
        path('delete/', views.delete_task, name='delete_task'),  # Изтриване на задача
        path('self-assessment/', views.SelfAssessmentView.as_view(), name='self_assessment'),  # Самооценка за задача

    ])),
]
