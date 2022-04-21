# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trigger', views.trigger, name='trigger'),
    path('<str:room_name>/', views.room, name='room'),
]
