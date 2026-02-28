from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/', views.update_task, name='update_task'),
    path('tasks/<int:pk>/report/', views.task_report, name='task_report'),
]
