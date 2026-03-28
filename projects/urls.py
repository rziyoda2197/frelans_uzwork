from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('my/', views.my_projects, name='my_projects'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('<int:pk>/proposal/', views.proposal_create, name='proposal_create'),
    path('<int:pk>/complete/', views.project_complete, name='project_complete'),
    path('proposal/<int:pk>/accept/', views.proposal_accept, name='proposal_accept'),
    path('proposal/<int:pk>/reject/', views.proposal_reject, name='proposal_reject'),
]
