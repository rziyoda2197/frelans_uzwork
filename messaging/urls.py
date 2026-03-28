from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox_view, name='inbox'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('chat/<str:username>/new/', views.get_new_messages, name='get_new_messages'),
    path('chat/<str:username>/send/', views.send_message_ajax, name='send_message_ajax'),
    path('unread/', views.unread_count, name='unread_count'),
]
