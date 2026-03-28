from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:project_pk>/', views.create_review, name='create_review'),
]
