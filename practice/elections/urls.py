from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('areas/<str:area>/', views.areas),
    path('polls/<int:poll_id>', views.polls),
]
