from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # User management (SuperAdmin only)
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    # Admin management (SuperAdmin only)
    path('admins/', views.admin_list, name='admin_list'),
    path('admins/create/', views.admin_create, name='admin_create'),
    path('admins/<int:pk>/update/', views.admin_update, name='admin_update'),
    path('admins/<int:pk>/delete/', views.admin_delete, name='admin_delete'),
    
    # User assignment (SuperAdmin only)
    path('assign-user/', views.assign_user_to_admin, name='assign_user'),
    
    # Task management
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/report/', views.task_report, name='task_report'),
]
