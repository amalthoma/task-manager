from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.web_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('web-logout/', views.web_logout, name='web_logout'),
    path('profile/', views.profile, name='profile'),
]
