from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:pk>/toggle/', views.toggle_user_active, name='toggle_user_active'),
    path('projects/', views.manage_projects, name='manage_projects_admin'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project_admin'),
]
